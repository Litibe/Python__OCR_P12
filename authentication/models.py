from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser


class ProfileStaff(models.Model):
    name = models.CharField(max_length=30,
                            verbose_name='Name Profile')
    manage_staff_user_crud = models.BooleanField(
        verbose_name=(
            'Manage Staff - CRUD method for User & Profile_staff'
            ), default=False)
    customer_read = models.BooleanField(
        verbose_name='Customer - Read', default=False)
    customer_CRU_assigned = models.BooleanField(
        verbose_name=(
            'Customer - CRU method for Customer.sales_contact assigned'
            ), default=False)
    customer_CRUD_all = models.BooleanField(
        verbose_name='Customer - CRUD ', default=False)
    contract_read = models.BooleanField(
        verbose_name='Contract - Read only', default=False)
    contract_CRU_assigned = models.BooleanField(
        verbose_name=(
            'Contract - CRU method for Customer.sales_contact assigned'
            ), default=False)
    contract_CRUD_all = models.BooleanField(
        verbose_name='Contract - CRUD method for all', default=False)
    event_read = models.BooleanField(
        verbose_name='Event - Read only', default=False)
    event_CRU_assigned = models.BooleanField(
        verbose_name=(
            'Event - CRU method for Event.support_contact assigned'
            ), default=False)
    event_CRUD_all = models.BooleanField(
        verbose_name='Event - CRUD method for all', default=False)
    need_read = models.BooleanField(
        verbose_name='Need - Read only', default=False)
    need_CRU_assigned = models.BooleanField(
        verbose_name=(
            'Need - CRU method for Event.support_contact assigned'
            ), default=False)
    need_CRUD_all = models.BooleanField(
        verbose_name='Need - CRUD method', default=False)

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
