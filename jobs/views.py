from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import Http404, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, FormView

from jobs.forms import ApplicationForm, RegistrationForm, LoginForm, MyCompanyForm
from jobs.models import Specialty, Vacancy, Company, Application


def custom_handler404(request, exception):
    return HttpResponseNotFound('Упс, не могу найти такую страницу...')


def custom_handler500(request, *args, **kwargs):
    return HttpResponseServerError('Упс, что то сломалось...')


class MainView(View):

    def get(self, request):
        context = {
            "specialties": Specialty.objects.all(),
            "companies": Company.objects.exclude(name=None),
        }

        return render(request, "index.html", context)


class VacanciesView(View):

    def get(self, request):
        context = {
            "category": "Все вакансии",
            "vacancies": Vacancy.objects.all(),
        }

        return render(request, "vacancies.html", context)


class SpecialtyView(View):

    def get(self, request, specialty: str):
        data = Specialty.objects.filter(code=specialty)
        if not data:
            raise Http404

        context = {
            "category": data.first().title,
            "vacancies": data.first().vacancies.all(),
        }

        return render(request, "vacancies.html", context)


class CompanyView(View):

    def get(self, request, company: int):
        if company not in Company.objects.values_list('id', flat=True):
            raise Http404

        context = {
            'company': Company.objects.get(id=company)
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
        }

        return render(request, "vacancy.html", context)

    def post(self, request, vacancy_id: int):
        application_form = ApplicationForm(request.POST)
        vacancy = Vacancy.objects.get(id=vacancy_id)

        if application_form.is_valid():
            if not Application.objects.filter(vacancy=vacancy, user=request.user).exists():
                data = application_form.cleaned_data
                Application.objects.create(
                    written_username=data['written_username'],
                    written_phone=data['written_phone'],
                    written_cover_letter=data['written_cover_letter'],
                    vacancy=vacancy,
                    user=request.user,
                )
                return render(request, "sent.html", {'url': request.build_absolute_uri()})
            else:
                application_form.add_error(None, 'Отправить отклик на вакансию можно только один раз :(')

        context = {
            'vacancy': vacancy,
            'form': application_form,
        }

        return render(request, "vacancy.html", context)


class MyCompanyView(UpdateView):
    model = Company
    form_class = MyCompanyForm
    template_name = "company-edit.html"
    success_url = "."

    def get_object(self):
        return Company.objects.get(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
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
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Информация о компании обновлена')
        return super().post(request, *args, **kwargs)


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
