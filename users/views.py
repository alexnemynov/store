from django.shortcuts import render
from django.contrib import auth, messages
from django.urls import reverse
from django.http import HttpResponseRedirect

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


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()  # вызывает save через менеджер objects и сохраняет данные в бд
            messages.success(request, 'Поздравляем! Вы успешно зарегистрированы!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/registration.html', context)


def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)
    context = {
        'title': 'Store - Профиль',
        'form': form,
        'baskets': Basket.objects.filter(user=request.user),
    }
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))