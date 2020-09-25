from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist, SuspiciousOperation
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q, Count
from django.http import Http404, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, UpdateView

from jobs.forms import ApplicationForm, RegistrationForm, LoginForm, MyCompanyForm, MyVacancyForm, ResumeForm, \
    SearchForm
from jobs.models import Specialty, Vacancy, Company, Application, Resume


def custom_handler404(request, exception):
    return HttpResponseNotFound('Упс, не могу найти такую страницу...')


def custom_handler500(request, *args, **kwargs):
    return HttpResponseServerError('Упс, что то сломалось...')


class MainView(View):

    def get(self, request):
        print(request.GET)
        if 's' in request.GET:
            return redirect(f"/search/?s={request.GET['s']}")

        companies = Company.objects.filter(name__isnull=False)\
            .annotate(vacancies_len=Count('vacancies', filter=Q(vacancies__title__isnull=False)))

        context = {
            "specialties": Specialty.objects.all(),
            "companies": companies,
            'form': SearchForm()
        }

        return render(request, "index.html", context)


class VacanciesView(View):

    def get(self, request):
        vacancies = Vacancy.objects.filter(title__isnull=False)
        context = {
            "category": "Все вакансии",
            "vacancies": vacancies,
        }

        return render(request, "vacancies.html", context)


class SpecialtyView(View):

    def get(self, request, specialty_code: str):
        try:
            specialty = Specialty.objects.get(code=specialty_code)
            vacancies = Vacancy.objects.filter(specialty=specialty)
        except ObjectDoesNotExist:
            raise Http404

        context = {
            "category": specialty.title,
            "vacancies": vacancies,
        }

        return render(request, "vacancies.html", context)


class CompanyView(View):

    def get(self, request, company_id: int):
        try:
            company = Company.objects.get(id=company_id)
            vacancies = Vacancy.objects.filter(title__isnull=False, company=company)
        except ObjectDoesNotExist:
            raise Http404

        context = {
            'company': company,
            'vacancies': vacancies,
            'previous_url': self.request.META['HTTP_REFERER'],
        }
        return render(request, "company.html", context)


class VacancyView(View):

    def get(self, request, vacancy_id: int):
        try:
            vacancy = Vacancy.objects.get(id=vacancy_id)
        except ObjectDoesNotExist:
            return redirect('/vacancies/')

        context = {
            'vacancy': vacancy,
            'form': ApplicationForm() if request.user.is_authenticated else None,
            'previous_url': self.request.META['HTTP_REFERER'],
        }

        return render(request, "vacancy.html", context)

    def post(self, request, vacancy_id: int):
        application_form = ApplicationForm(request.POST)
        try:
            vacancy = Vacancy.objects.get(id=vacancy_id)
        except ObjectDoesNotExist:
            return HttpResponseServerError

        if application_form.is_valid():
            if not Application.objects.filter(vacancy=vacancy, user=request.user).exists():
                if application_form.is_valid():
                    data = application_form.cleaned_data
                    Application.objects.create(
                        written_username=data['written_username'],
                        written_phone=data['written_phone'],
                        written_cover_letter=data['written_cover_letter'],
                        vacancy=vacancy,
                        user=request.user,
                    )
                elif "written_phone" not in application_form.cleaned_data:
                    application_form.add_error("written_phone", 'Некорректный формат номера телефона')
                else:
                    raise SuspiciousOperation("Invalid request")

                return render(request, "sent.html", {'vacancy_id': vacancy_id})
            else:
                application_form.add_error(None, 'Отправить отклик на вакансию можно только один раз :(')

        context = {
            'vacancy': vacancy,
            'form': application_form,
        }

        return render(request, "vacancy.html", context)


class MyCompanyEditView(UpdateView):
    model = Company
    form_class = MyCompanyForm
    template_name = "company-edit.html"
    success_url = "."

    def get_object(self):
        return Company.objects.get(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            return super().get(request, *args, **kwargs)
        except ObjectDoesNotExist:
            Company.objects.create(
                name=None,
                logo=None,
                location=None,
                description=None,
                employee_count=None,
                owner=request.user,
            )
            return render(request, "company-create.html")

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Информация о компании обновлена')
        return super().post(request, *args, **kwargs)


class MyVacancy(View):

    def get(self, request, vacancy_id: int):
        try:
            company = Company.objects.get(owner=request.user)
            context = {
                "vacancy": company.vacancies.get(id=vacancy_id),
                'form': ApplicationForm(),
            }

            return render(request, "vacancy.html", context)

        except ObjectDoesNotExist:
            raise Http404


class MyVacancies(View):

    def get(self, request):
        try:
            company = Company.objects.get(owner=request.user)

            context = {
                "category": company.name,
                "vacancies": company.vacancies.all(),
            }

            return render(request, "vacancies.html", context)

        except ObjectDoesNotExist:
            raise Http404


class MyVacanciesListView(View):

    def get(self, request):
        vacancies = Vacancy.objects.\
            filter(company__owner=request.user).\
            annotate(applications_count=Count('applications'))

        context = {
            'vacancies': vacancies,
        }
        return render(request, "vacancy-list.html", context)


class MyVacanciesEditView(UpdateView):
    model = Vacancy
    form_class = MyVacancyForm
    template_name = "vacancy-edit.html"
    success_url = "."

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Вакансия обновлена')
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.published_at = datetime.now()
        self.object.save()
        return super(MyVacanciesEditView, self).form_valid(form)


class CreateMyVacancy(View):

    def get(self, request):
        try:
            new_vacancy = Vacancy.objects.create(
                company=Company.objects.get(owner=request.user)
            )
            return redirect(f'/mycompany/vacancies-edit/{new_vacancy.pk}')

        except ObjectDoesNotExist:
            raise HttpResponseServerError


class ResumeCreateView(View):

    def get(self, request):
        return render(request, "resume-create.html")

    def post(self, request):
        if not Resume.objects.filter(user=request.user).exists():
            Resume.objects.create(user=request.user)
        return redirect('/myresume/')


class ResumeEditView(UpdateView):
    model = Resume
    form_class = ResumeForm
    template_name = "resume-edit.html"
    success_url = '.'

    def get_object(self):
        return Resume.objects.get(user=self.request.user)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            return super().get(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return redirect('/myresume/create')

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Ваше резюме обновлено!')
        return super().post(request, *args, **kwargs)


class SearchView(View):

    def get(self, request):
        """
        Поиск не работает с русскими фразами в unicode. Из-за использования sqlite?
        """
        try:
            query = request.GET['s']
        except KeyError:
            query = None

        if query:
            vacancies = Vacancy.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        else:
            vacancies = None

        context = {
            'query': query,
            'vacancies': vacancies,
            'form': SearchForm(initial={'s': query}),
        }
        return render(request, "search.html", context)


class MyLoginView(LoginView):
    form_class = LoginForm
    redirect_authenticated_user = True
    template_name = 'login.html'


class MyLogoutView(LogoutView):
    next_page = '/'


class MySignupView(CreateView):
    form_class = RegistrationForm
    success_url = 'login/'
    template_name = 'register.html'
