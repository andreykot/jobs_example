from crispy_forms.bootstrap import FormActions, AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, HTML, Div, Row, Column
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from jobs.models import Company


class ApplicationForm(forms.Form):
    written_username = forms.CharField(max_length=200, label='Вас зовут')
    written_phone = forms.CharField(max_length=16, label='Ваш телефон')
    written_cover_letter = forms.CharField(max_length=2000, widget=forms.Textarea, label='Сопроводительное письмо')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-group'

        self.helper.layout = Layout(
            Fieldset(
                'Отозваться на вакансию',
                AppendedText('written_username', '', placeholder="ФИО"),
                AppendedText('written_phone', '', placeholder="+78001010101"),
                AppendedText('written_cover_letter', '', placeholder="Сопроводительное письмо"),
            ),
            FormActions(
                Submit('submit', 'Записаться на пробный урок')
            )
        )


class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=100, label='Логин')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = "form-signin pt-5"

        self.helper.layout = Layout(
            Div(
                HTML('<h1 class="h3 mb-3 font-weight-normal">Джуманджи</h1>'),
                HTML('<p class="h5 font-weight-light">Создайте аккаунт</p>'),
                css_class="text-center mt-5 b-1"
            ),
            Div(
                "username",
                "first_name",
                "last_name",
                "password1",
                "password2",
                FormActions(
                    Submit('submit', 'Зарегистрироваться'),
                    css_class="btn btn-primary btn-lg btn-block",
                )
            )
        )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2"
        )


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, label='Логин')

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = "form-signin pt-5"

        self.helper.layout = Layout(
            Div(
                HTML('<h1 class="h3 mb-3 font-weight-normal">Джуманджи</h1>'),
                HTML('<p class="h5 font-weight-light">Вход</p>'),
                css_class="text-center mt-5 b-1"
            ),
            Div(
                "username",
                "password",
                FormActions(
                    Submit('submit', 'Войти'),
                    css_class="btn btn-primary btn-lg btn-block",
                )
            )
        )

    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )


class MyCompanyForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Название компании')
    location = forms.CharField(max_length=200, label='География')
    logo = forms.ImageField(label='Логотип')
    description = forms.CharField(widget=forms.Textarea, label='Информация о компании')
    employee_count = forms.IntegerField(min_value=0, label='Количество человек в компании')

    class Meta:
        model = Company
        fields = (
            "name",
            "location",
            "logo",
            "description",
            "employee_count",
        )
