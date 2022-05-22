from datetime import datetime
from django.conf import settings
from rest_framework.serializers import ModelSerializer
from rest_framework import fields

from crm.models import Customer, Contract, Event, Need
from authentication.serializers import UserSerializer, UserSerializerRead


class CustomerSerializer(ModelSerializer):
    id = fields.CharField(read_only=True)
    first_name = fields.CharField(required=True, max_length=25)
    last_name = fields.CharField(required=True, max_length=25)
    email = fields.EmailField(required=True, max_length=100)
    phone = fields.CharField(required=True, max_length=25)
    mobile = fields.CharField(required=True, max_length=25)
    company_name = fields.CharField(required=True, max_length=250)
    sales_contact = UserSerializerRead(many=False, read_only=True)

    class Meta:
        model = Customer
        fields = [
            "id", "first_name", "last_name", "email",
            "phone", "mobile", "company_name", "sales_contact"]

    def create(self, validated_data, user_sales_contact):
        customer = Customer.objects.create(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            phone=validated_data["phone"],
            mobile=validated_data["mobile"],
            company_name=validated_data["company_name"],
            sales_contact=user_sales_contact)
        customer.save()
        return True

    def put(self, validated_data, pk, user_sales_contact):
        customer = Customer.objects.filter(id=pk).first()
        customer.first_name = validated_data["first_name"]
        customer.last_name = validated_data["last_name"]
        customer.email = validated_data["email"]
        customer.phone = validated_data["phone"]
        customer.mobile = validated_data["mobile"]
        customer.company_name = validated_data["company_name"]
        customer.sales_contact = user_sales_contact
        customer.save()
        return True

    def delete(self, pk):
        customer = Customer.objects.filter(id=pk).first()
        customer.delete()
        return True


class ContractSerializer(ModelSerializer):
    id = fields.CharField(read_only=True)
    title = fields.CharField(required=True, max_length=125)
    date_start_contract = fields.DateTimeField(
        format=settings.DATETIME_FORMAT,
        input_formats=settings.DATETIME_INPUT_FORMAT,
        default_timezone=None)
    date_end_contract = fields.DateTimeField(
        required=True, input_formats=['%Y-%m-%d %H:%M'])
    signed = fields.BooleanField(default=False)
    customer_assigned = CustomerSerializer(many=False, read_only=True)

    class Meta:
        model = Contract
        fields = [
            'id', 'title', 'date_start_contract',
            'date_end_contract', 'signed', 'customer_assigned']
        depth = 2

    def create(self, validated_data, customer):
        contract = Contract.objects.create(
            title=validated_data["title"],
            date_start_contract=validated_data["date_start_contract"],
            date_end_contract=validated_data["date_end_contract"],
            signed=validated_data["signed"],
            customer_assigned=customer)
        contract.save()
        return True

    def put(self, validated_data, pk, customer):
        contract = Contract.objects.filter(id=pk).first()
        contract.title = validated_data["title"]
        contract.date_start_contract = validated_data["date_start_contract"]
        contract.date_end_contract = validated_data["date_end_contract"]
        contract.signed = validated_data["signed"]
        contract.customer_assigned = customer
        contract.save()
        return True

    def delete(self, pk):
        contract = Contract.objects.filter(id=pk).first()
        contract.delete()
        return True


class EventSerializer(ModelSerializer):
    id = fields.CharField(read_only=True)
    support_contact = UserSerializerRead(many=False, read_only=True)
    contract_assigned = ContractSerializer(many=False, read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'date_started', 'date_finished',
                  'date_updated', 'support_contact', 'contract_assigned']

    def create(self, validated_data, support_contact, contract_assigned):
        event = Event.objects.create(
            title=validated_data["title"],
            date_started=validated_data["date_started"],
            date_finished=validated_data["date_finished"],
            date_updated=datetime.now(),
            support_contact=support_contact,
            contract_assigned=contract_assigned)
        event.save()
        return True

    def put(
            self, validated_data, id_event,
            support_contact, contract_assigned):
        event = Event.objects.filter(id=id_event).first()
        event.title = validated_data["title"]
        event.date_started = validated_data["date_started"]
        event.date_finished = validated_data["date_finished"]
        event.date_updated = datetime.now()
        event.support_contact = support_contact
        event.contract_assigned = contract_assigned
        event.save()
        return True

    def delete(self, pk):
        event = Event.objects.filter(id=pk).first()
        event.delete()
        return True


class NeedSerializer(ModelSerializer):
    id = fields.CharField(read_only=True)
    event_assigned = EventSerializer(many=False, read_only=True)

    class Meta:
        model = Need
        fields = ['id', 'title', 'success',
                  'date_updated', 'event_assigned']

    def create(self, validated_data, event_assigned):
        need = Need.objects.create(
            title=validated_data["title"],
            success=validated_data["success"],
            date_updated=datetime.now(),
            event_assigned=event_assigned)
        need.save()
        return True

    def put(
            self, validated_data, id_need,
            event_assigned):
        need = Need.objects.filter(id=id_need).first()
        need.title = validated_data["title"]
        need.success = validated_data["success"]
        need.date_updated = datetime.now()
        need.event_assigned = event_assigned
        need.save()
        return True

    def delete(self, pk):
        need = Need.objects.filter(id=pk).first()
        need.delete()
        return True
