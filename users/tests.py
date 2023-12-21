from django import setup
setup()


from django.test import TestCase
from django.urls import reverse


class UserRegistrationView(TestCase)

    def setUp(self):
        self.path = reverse('users:registration')

