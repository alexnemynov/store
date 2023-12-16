from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from products.models import Basket


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


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.request.user)  # можно user=self.object
        return context


    def get_object(self, queryset=None):  # вместо profile/<int:pk>, а остальное под "капотом" делается
        return self.request.user