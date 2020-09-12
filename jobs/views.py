from django.http import Http404
from django.shortcuts import render

# Create your views here.
from django.views import View


class MainView(View):

    def get(self, request):
        return render(request, "index.html")


class VacanciesView(View):

    def get(self, request):
        return render(request, "vacancies.html")


class SpecialtyView(View):

    def get(self, request, specialty: str):
        if specialty != 'frontend':
            raise Http404

        return render(request, "vacancies.html")


class CompanyView(View):

    def get(self, request, company: int):
        if company != 345:
            raise Http404

        return render(request, "company.html")


class VacancyView(View):

    def get(self, request, vacancy: int):
        if vacancy != 22:
            raise Http404

        return render(request, "vacancy.html")
