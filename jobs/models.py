from django.db import models


class Specialty(models.Model):
    code = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    picture = models.CharField(max_length=2000)


class Company(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    logo = models.CharField(max_length=2000)
    description = models.TextField()
    employee_count = models.IntegerField(null=True)


class Vacancy(models.Model):
    title = models.CharField(max_length=200)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.TextField()
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField()
