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
    event_create = models.BooleanField(verbose_name='Event - Create',
                                       default=False)
    event_read = models.BooleanField(verbose_name='Event - Read',
                                     default=False)
    event_update = models.BooleanField(verbose_name='Event - Update',
                                       default=False)
    event_delete = models.BooleanField(verbose_name='Event - Delete',
                                       default=False)
    need_create = models.BooleanField(verbose_name='Need - Create',
                                      default=False)
    need_read = models.BooleanField(verbose_name='Need - Read',
                                    default=False)
    need_update = models.BooleanField(verbose_name='Need - Update',
                                      default=False)
    need_delete = models.BooleanField(verbose_name='Need - Delete',
                                      default=False)

    def __str__(self):
        return f'{self.name}'


class User(AbstractUser):
    date_joined = models.DateTimeField(default=timezone.now)
    email = models.EmailField(
        max_length=256, verbose_name="email", unique=True)
    username = None
    profile_staff = models.ForeignKey(to=ProfileStaff,
                                      on_delete=models.SET_NULL,
                                      null=True,
                                      verbose_name="Profile Staff Name",
                                      related_name="Profile_Staff_name")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "profile_staff"]

