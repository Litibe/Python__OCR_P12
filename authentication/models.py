from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    MANAGE = 'MANAGE'
    SALES = "SALES"
    SUPPORT = 'SUPPORT'

    ROLE_CHOICES = (
        (MANAGE, 'EQ_Gestion'),
        (SALES, 'EQ_Ventes'),
        (SUPPORT, 'EQ_Support'),
    )

    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField('staff', default=True)
    is_superuser = models.BooleanField('superuser', default=False)
    username = models.CharField(max_length=128, blank=True, unique=False)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=128, verbose_name="First Name")
    last_name = models.CharField(max_length=128, verbose_name="Last Name")
    email = models.EmailField(
        max_length=256, verbose_name="email", unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle')
