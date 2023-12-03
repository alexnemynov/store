from django.shortcuts import render
from django.contrib import auth
from django.urls import reverse
from django.http import HttpResponseRedirect

from users.models import User
from users.forms import UserLoginForm


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
    return render(request, 'users/registration.html')
