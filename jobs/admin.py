from django.contrib import admin

from jobs.models import Company, Vacancy, Application, Specialty


class SpecialtiesAdmin(admin.ModelAdmin):
    pass


class CompaniesAdmin(admin.ModelAdmin):
    pass


class VacanciesAdmin(admin.ModelAdmin):
    pass


class ApplicationsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Specialty, SpecialtiesAdmin)
admin.site.register(Company, CompaniesAdmin)
admin.site.register(Vacancy, VacanciesAdmin)
admin.site.register(Application, ApplicationsAdmin)
