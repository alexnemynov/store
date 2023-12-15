from django.shortcuts import render
from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from products.models import Basket


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']  # извлекаем данные из POST запроса
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password) # извлекаем данные из бд, чтобы проверить, есть ли такой пользователь
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))  # если логин прошел успешно, то перенаправляем на главную страницу
                # 'index' - название из path('', index, name='index')... (см. urls.py в главной папке проекта)
                # можно было просто '/' написать без reverse, но так сохраняется относительный путь
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    extra_context = {'title': 'Регистрация'}


class UserProfileView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    extra_context = {'title': 'Личный кабинет'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Store - Личный кабинет'
        context['baskets'] = Basket.objects.filter(user=self.request.user)  # можно user=self.object
        return context

    def get_object(self, queryset=None):  # вместо profile/<int:pk>, а остальное под "капотом" делается
        return self.request.user


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


# def registration(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()  # вызывает save через менеджер objects и сохраняет данные в бд
#             messages.success(request, 'Поздравляем! Вы успешно зарегистрированы!')
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = UserRegistrationForm()
#     context = {'form': form}
#     return render(request, 'users/registration.html', context)


# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users:profile'))
#         else:
#             print(form.errors)
#     else:
#         form = UserProfileForm(instance=request.user)
#     context = {
#         'title': 'Store - Профиль',
#         'form': form,
#         'baskets': Basket.objects.filter(user=request.user),
#     }
#     return render(request, 'users/profile.html', context)