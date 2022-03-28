from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class profile_choices(models.TextChoices):
        MANAGE = 'MANAGE'
        SALES = 'SALES'
        SUPPORT = 'SUPPORT'
    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField('staff', default=True)
    is_superuser = models.BooleanField('superuser', default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=128, verbose_name="First Name")
    last_name = models.CharField(max_length=128, verbose_name="Last Name")
    email = models.EmailField(
        max_length=256, verbose_name="email", unique=True)
    username = models.CharField(max_length=128, blank=True, unique=False)
    profile = models.CharField(max_length=30,
                               choices=profile_choices.choices,
                               default='SALES',
                               verbose_name='Profile')
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "profile"]
