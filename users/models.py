from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)  # Подтвердил ли пользователь эл почту
    email = models.EmailField(unique=True)


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)  # формирование уникального идентификатора
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)  # автозаполнение даты и времени создания
    expiration = models.DateTimeField()  # для контроля времени жизни ссылки, заполнять вручную будем

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'

    def send_verification_email(self):
        link = reverse('users:email_verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение учетной записи для {self.user.username}'
        message = 'Для подтверждения учетной записи для {} перейдите по ссылке: {}'.format(
            self.user.email,
            verification_link
        )
        html_message = 'Для подтверждения учетной записи для {} перейдите по <a href="{}">ссылке</a>'.format(
            self.user.email,
            verification_link
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
            html_message=html_message,
        )

    def is_expired(self):
        return True if now() >= self.expiration else False
