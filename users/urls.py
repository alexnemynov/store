from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import (EmailVerificationView, UserLoginView, UserProfileView,
                         UserRegistrationView)

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),  # ../users/login/
    path('registration/', UserRegistrationView.as_view(), name='registration'),  # ../users/registration/
    path('profile/', UserProfileView.as_view(), name='profile'),  # ../users/profile/
    path('logout/', LogoutView.as_view(), name='logout'),  # ../users/profile/logout
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email_verification'),  # ../users/v..
]
