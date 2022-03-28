from datetime import timezone
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
    company_name = models.CharField(max_length=250, verbose_name="Compagny Name")
    date_created = models.DateTimeField(verbose_name="Date Created")
    date_updated = models.DateTimeField(verbose_name="Date Updated")
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)