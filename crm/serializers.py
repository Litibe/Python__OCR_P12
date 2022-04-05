from rest_framework.serializers import ModelSerializer, EmailField, CharField
from rest_framework import fields

from crm.models import Customer, Contract, Event, Need
from authentication.serializers import UserSerializer


class CustomerSerialiser(ModelSerializer):
    first_name = fields.CharField(required=True, max_length=25)
    last_name = fields.CharField(required=True, max_length=25)
    email = fields.EmailField(required=True, max_length=100)
    phone = fields.CharField(required=True, max_length=25)
    mobile = fields.CharField(required=True, max_length=25)
    company_name = fields.CharField(required=True, max_length=250)
    sales_contact = UserSerializer(many=False)

    class Meta:
        model = Customer