from django.utils import timezone
from django.conf import settings
from django.db import models


class Customer(models.Model):
    """ 
    Class Object Customer
    """
    first_name = models.CharField(max_length=25, verbose_name="First Name")
    last_name = models.CharField(max_length=25, verbose_name="Last Name")
    email = models.EmailField(
        max_length=100, verbose_name="email", unique=True)
    phone = models.CharField(max_length=20, verbose_name="Phone Number")
    mobile = models.CharField(max_length=20, verbose_name="Mobile Number")
    company_name = models.CharField(max_length=250, 
                                    verbose_name="Compagny Name")
    date_created = models.DateTimeField(
        verbose_name="Date Created", default=timezone.now)
    date_updated = models.DateTimeField(
        verbose_name="Date Updated", default=timezone.now)
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        limit_choices_to={'profile_staff': 2},
        on_delete=models.CASCADE)


class Contract(models.Model):
    """
    Class Object Contract for Customer
    """
    date_created = models.DateTimeField(
        verbose_name="Date Start Contract", default=timezone.now)
    date_finished = models.DateTimeField(
        verbose_name="Date End Contract", default=timezone.now)
    signed = models.BooleanField('signed', default=False)
    customer_assigned = models.ForeignKey(
        to=Customer, on_delete=models.CASCADE)


class Event(models.Model):
    """
    Class Object Event
    """
    title = models.CharField(max_length=125, verbose_name="Title Event")
    date_created = models.DateTimeField(
        verbose_name="Date Start", default=timezone.now)
    date_updated = models.DateTimeField(
        verbose_name="Date Updated", default=timezone.now)
    date_finished = models.DateTimeField(verbose_name="Date End")
    support_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        limit_choices_to={'profile_staff': 3},
        on_delete=models.CASCADE)
    contract_assigned = models.ForeignKey(
        to=Contract, on_delete=models.CASCADE)


class Need(models.Model):
    """
    Class Object Need For Event
    """
    title = models.CharField(max_length=125, verbose_name="title Need")
    success = models.BooleanField('signed', default=False)
    date_updated = models.DateTimeField(
        verbose_name="Date Updated", default=timezone.now)
    event_assigned = models.ForeignKey(
        to=Event, on_delete=models.CASCADE)
