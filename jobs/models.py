from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Specialty(models.Model):
    code = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    picture = models.ImageField(upload_to=settings.MEDIA_SPECIALITY_IMAGE_DIR)

    def __str__(self):
        return f"{self.title}"


class Company(models.Model):
    name = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=200, null=True)
    logo = models.ImageField(upload_to=settings.MEDIA_COMPANY_IMAGE_DIR, null=True)
    description = models.TextField(blank=True, null=True)
    employee_count = models.PositiveIntegerField(blank=True, null=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Company({self.name}, {self.location}, {self.logo}, " \
               f"{self.description}, {self.employee_count}, {self.owner})"


class Vacancy(models.Model):
    title = models.CharField(max_length=200, null=True)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies', null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.TextField(null=True)
    description = models.TextField(null=True)
    salary_min = models.PositiveIntegerField(null=True)
    salary_max = models.PositiveIntegerField(null=True)
    published_at = models.DateField(null=True)

    def __str__(self):
        return f"Company({self.title}, {self.specialty}, {self.company}, " \
               f"{self.skills}, {self.description}, {self.salary_min}, {self.salary_max}, " \
               f"{self.published_at})"


class Application(models.Model):
    written_username = models.CharField(max_length=200)
    written_phone = models.CharField(max_length=16)
    written_cover_letter = models.CharField(max_length=2000)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')

    def __str__(self):
        return f"Specialty({self.written_username}, {self.written_phone}, {self.written_cover_letter}, " \
               f"{self.vacancy}, {self.user})"


class Resume(models.Model):

    class STATUS(models.TextChoices):
        NOT_LOOKING = 1, "Не ищу работу"
        CONSIDERING = 2, "Рассматриваю предложения"
        LOOKING = 3, "Ищу работу"

    class GRADE(models.TextChoices):
        TRAINEE = 1, "Стажер"
        JUNIOR = 2, "Junior"
        MIDDLE = 3, "Middle"
        SENIOR = 4, "Senior"
        LEAD = 5, "Lead"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    surname = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, choices=STATUS.choices, null=True)
    salary = models.PositiveIntegerField(null=True)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='resume', null=True)
    grade = models.CharField(max_length=100, choices=GRADE.choices, null=True)
    education = models.TextField(null=True)
    experience = models.TextField(null=True)
    portfolio = models.TextField(null=True)

    def __str__(self):
        return f"Resume ({self.name}, {self.surname})"
