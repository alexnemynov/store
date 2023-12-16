import uuid
from datetime import timedelta

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, get_user_model
from django.utils.timezone import now

from .models import EmailVerification


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={  # TextInput не скрывается, а PasswordInput скрывается
        'class': 'form-control py-4', 'placeholder': 'Введите пароль'}))

    class Meta:
        model = get_user_model()  # он будет хватать переменную в settings.py AUTH_USER_MODEL = 'users.User'
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите Фамилию'}))
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'}))
    email = forms.CharField(label='Адрес электронной почты', widget=forms.EmailInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите адрес эл. почты'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=True)
        expiration = now() + timedelta(days=2)
        record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
        record.send_verification_email()

        return user


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={  # тут нет placeholder, тк данные заполнены!
        'class': 'form-control py-4'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={
        'class': 'form-control py-4'}))
    image = forms.ImageField(label='Выберите изображение', widget=forms.FileInput(attrs={
        'class': 'custom-file-label'}), required=False)  # поле необяз к заполнению, иначе без картинки не сохр форму!
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'readonly': True}))  # только для чтения
    email = forms.CharField(label='Адрес электронной почты', widget=forms.EmailInput(attrs={
        'class': 'form-control py-4', 'readonly': True}))

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'image', 'username', 'email')