from django.http import Http404, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render
from django.views import View
from jobs.models import Specialty, Vacancy, Company


def custom_handler404(request, exception):
    return HttpResponseNotFound('Упс, не могу найти такую страницу...')


def custom_handler500(request, *args, **kwargs):
    return HttpResponseServerError('Упс, что то сломалось...')


class MainView(View):

    def get(self, request):
        specialties = [specialty for specialty in Specialty.objects.all()]
        companies = [company for company in Company.objects.all()]
        context = {
            "specialties_line1": specialties[:4],
            "specialties_line2": specialties[4:],
            "companies_line1": companies[:4],
            "companies_line2": companies[4:],
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

    def get(self, request, vacancy: int):
        if vacancy not in Vacancy.objects.values_list('id', flat=True):
            raise Http404

        context = {
            'vacancy': Vacancy.objects.get(id=vacancy)
        }

        return render(request, "vacancy.html", context)
