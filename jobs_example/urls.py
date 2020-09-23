"""jobs_example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from jobs.views import MainView, VacanciesView, SpecialtyView, CompanyView, VacancyView, \
    custom_handler404, custom_handler500, MySignupView, MyLoginView, MyLogoutView, MyCompanyView, MyVacancies, \
    MyVacancy, MyVacanciesEditView, MyVacanciesListView, CreateMyVacancy

handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view()),
    path('vacancies/', VacanciesView.as_view()),
    path('vacancies/cat/<str:specialty>/', SpecialtyView.as_view()),
    path('companies/<int:company_id>/', CompanyView.as_view()),
    path('vacancies/<int:vacancy_id>/', VacancyView.as_view()),
    path('signup/login/', MyLoginView.as_view()),
    path('mycompany/', MyCompanyView.as_view()),
    path('mycompany/create-vacancy/', CreateMyVacancy.as_view()),
    path('mycompany/vacancies-edit/', MyVacanciesListView.as_view()),
    path('mycompany/vacancies-edit/<int:pk>/', MyVacanciesEditView.as_view()),
    path('mycompany/vacancies/', MyVacancies.as_view()),
    path('mycompany/vacancies/<int:vacancy_id>/', MyVacancy.as_view()),
]

urlpatterns += [
    path('login/', MyLoginView.as_view()),
    path('logout/', MyLogoutView.as_view()),
    path('signup/', MySignupView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
