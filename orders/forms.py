from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Иван'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Иванов'}))
    email = forms.EmailField(label='Адрес электронной почты', widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'you@example.com'}))
    address = forms.CharField(label='Адрес', widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Россия, Москва, ул. Мира, дом 6'}))

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address']
