from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from products.models import Basket
from .models import User, EmailVerification


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    extra_context = {'title': 'Store - Авторизация'}

    def get_success_url(self):
        return reverse_lazy('index')


class UserRegistrationView(SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    extra_context = {'title': 'Store - Регистрация'}
    success_message = 'Поздравляем! Вы успешно зарегистрированы!'


class UserProfileView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    extra_context = {'title': 'Store - Личный кабинет'}

    def get_object(self, queryset=None):  # вместо profile/<int:pk>, а остальное под "капотом" делается
        return self.request.user


class EmailVerificationView(TemplateView):
    extra_context = {'title': 'Store - Подтверждение электронной почты'}
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)

        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))


