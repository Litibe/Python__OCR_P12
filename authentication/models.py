from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser


class ProfileStaff(models.Model):
    name = models.CharField(max_length=30, default="Null",
                            verbose_name='Name Profile')
    manage_staff_create_user = models.BooleanField(verbose_name='Staff - Create User',
                                                   default=False)
    manage_staff_read_user = models.BooleanField(verbose_name='Staff - Read User',
                                                 default=False)
    manage_staff_update_user = models.BooleanField(verbose_name='Staff - Update User',
                                                   default=False)
    manage_staff_delete_user = models.BooleanField(verbose_name='Staff - Delete User',
                                                   default=False)
    customer_create = models.BooleanField(verbose_name='Customer - Create',
                                          default=False)
    customer_read = models.BooleanField(verbose_name='Customer - Read',
                                        default=False)
    customer_update = models.BooleanField(verbose_name='Customer - Update',
                                          default=False)
    customer_delete = models.BooleanField(verbose_name='Customer - Delete',
                                          default=False)
    contract_create = models.BooleanField(verbose_name='Contract - Create',
                                          default=False)
    contract_read = models.BooleanField(verbose_name='Contract - Read',
                                        default=False)
    contract_update = models.BooleanField(verbose_name='Contract - Update',
                                          default=False)
    contract_delete = models.BooleanField(verbose_name='Contract - Delete',
                                           default=False)

    def __str__(self):
        return f'{self.name}'

class User(AbstractUser):
    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField('staff', default=True)
    is_superuser = models.BooleanField('superuser', default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=128, verbose_name="First Name")
    last_name = models.CharField(max_length=128, verbose_name="Last Name")
    email = models.EmailField(
        max_length=256, verbose_name="email", unique=True)
    username = models.CharField(max_length=128, blank=True, unique=False)
    profile_staff = models.ForeignKey(to=ProfileStaff,
                                      on_delete=models.SET_NULL,
                                      null=True,
                                      verbose_name="Profile Staff Name",
                                      related_name="Profile_Staff_name")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "profile_staff"]