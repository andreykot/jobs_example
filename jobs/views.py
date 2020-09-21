from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import Http404, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView

from jobs.forms import ApplicationForm, RegistrationForm, LoginForm
from jobs.models import Specialty, Vacancy, Company, Application


def custom_handler404(request, exception):
    return HttpResponseNotFound('Упс, не могу найти такую страницу...')


def custom_handler500(request, *args, **kwargs):
    return HttpResponseServerError('Упс, что то сломалось...')


class MainView(View):

    def get(self, request):
        context = {
            "specialties": Specialty.objects.all(),
            "companies": Company.objects.all(),
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
        if not Vacancy.objects.filter(id=vacancy_id).exists():  # TODO
            raise Http404

        context = {
            'vacancy': Vacancy.objects.get(id=vacancy_id),
            'form': ApplicationForm(),
        }

        return render(request, "vacancy.html", context)

    def post(self, request, vacancy_id: int):
        """https://docs.djangoproject.com/en/3.1/topics/auth/default/"""

        if not request.user.is_authenticated:
            return HttpResponseServerError

        if not User.objects.filter(id=request.user.id).exists():
            return redirect('/signup/')

        application_form = ApplicationForm(request.POST)
        vacancy = Vacancy.objects.get(id=vacancy_id)
        if application_form.is_valid():
            if Application.objects.filter(
                    vacancy=vacancy,
                    user=request.user.id).\
                    exists():
                application_form.add_error('submit', 'Вы уже отправили заявку')
                return redirect('/')

            data = application_form.cleaned_data
            Application.objects.create(
                written_username=data['written_username'],
                written_phone=data['written_phone'],
                written_cover_letter=data['written_cover_letter'],
                vacancy=vacancy,
                user=request.user,
            )

            return render(request, "sent.html", {'url': request.build_absolute_uri()})

        elif "written_username" not in application_form.cleaned_data:
            application_form.add_error('written_username', 'Вы не указали свое имя')

        elif "written_phone" not in application_form.cleaned_data:
            application_form.add_error('written_username', 'Вы не указали свой телефон')

        elif "written_cover_letter" not in application_form.cleaned_data:
            application_form.add_error('written_username', 'Вы не написали сопроводительное письмо')

        else:
            return HttpResponseServerError()


class MyCompany(View):

    def get(self, request):
        try:
            context = {
                'company': Company.objects.get(owner_id=request.user.id)
            }
            return render(request, "company.html", context)

        except ObjectDoesNotExist:
            return render(request, "company-create.html")


class MyVacancies(View):

    def get(self, request):
        try:
            company = Company.objects.get(owner_id=request.user.id)

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
            company = Company.objects.get(owner_id=request.user.id)
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


class MySignupView(CreateView):
    form_class = RegistrationForm
    success_url = 'login/'
    template_name = 'register.html'
