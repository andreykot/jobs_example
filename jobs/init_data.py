# flake8: noqa

from datetime import datetime
import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jobs_example.settings")
django.setup()


from jobs.models import Vacancy, Company, Specialty


jobs = [

    {"title": "Разработчик на Python", "cat": "backend", "company": "staffingsmarter", "salary_from": "100000",
     "salary_to": "150000", "posted": "2020-03-11", "desc": "Потом добавим"},
    {"title": "Разработчик в проект на Django", "cat": "backend", "company": "swiftattack", "salary_from": "80000",
     "salary_to": "90000", "posted": "2020-03-11", "desc": "Потом добавим"},
    {"title": "Разработчик на Swift в аутсорс компанию", "cat": "backend", "company": "swiftattack",
     "salary_from": "120000", "salary_to": "150000", "posted": "2020-03-11", "desc": "Потом добавим"},
    {"title": "Мидл программист на Python", "cat": "backend", "company": "workiro", "salary_from": "80000",
     "salary_to": "90000", "posted": "2020-03-11", "desc": "Потом добавим"},
    {"title": "Питонист в стартап", "cat": "backend", "company": "primalassault", "salary_from": "120000",
     "salary_to": "150000", "posted": "2020-03-11", "desc": "Потом добавим"}

]

""" Компании """

companies = [

    {"title": "workiro"},
    {"title": "rebelrage"},
    {"title": "staffingsmarter"},
    {"title": "evilthreat h"},
    {"title": "hirey "},
    {"title": "swiftattack"},
    {"title": "troller"},
    {"title": "primalassault"}

]

""" Категории """

specialties = [

    {"code": "frontend", "title": "Фронтенд"},
    {"code": "backend", "title": "Бэкенд"},
    {"code": "gamedev", "title": "Геймдев"},
    {"code": "devops", "title": "Девопс"},
    {"code": "design", "title": "Дизайн"},
    {"code": "products", "title": "Продукты"},
    {"code": "management", "title": "Менеджмент"},
    {"code": "testing", "title": "Тестирование"}

]


if __name__ == '__main__':
    Company.objects.bulk_create(
        [
            Company(
                name=company['title'],
                logo="https://place-hold.it/100x60",
            )
            for company in companies
        ]
    )

    Specialty.objects.bulk_create(
        [
            Specialty(
                code=spec['code'],
                title=spec['title'],
                picture="https://place-hold.it/100x60"
            )
            for spec in specialties
        ]
    )

    Vacancy.objects.bulk_create(
        [
           Vacancy(
               title=job['title'],
               company=Company.objects.get(name=job['company']),
               specialty=Specialty.objects.get(code=job['cat']),
               description=job['desc'],
               salary_min=int(job['salary_from']),
               salary_max=int(job['salary_to']),
               published_at=datetime.strptime(job['posted'], "%Y-%m-%d").date()
           )
            for job in jobs
        ]
    )
