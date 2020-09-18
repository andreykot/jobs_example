from django.contrib import admin

from jobs.models import Company, Vacancy, Application


class CompaniesAdmin(admin.ModelAdmin):
    pass


class VacanciesAdmin(admin.ModelAdmin):
    pass


class ApplicationsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Company, CompaniesAdmin)
admin.site.register(Vacancy, VacanciesAdmin)
admin.site.register(Application, ApplicationsAdmin)
