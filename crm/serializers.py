from datetime import date
from rest_framework.serializers import ModelSerializer
from rest_framework import fields

from crm.models import Customer, Contract
from authentication.serializers import UserSerializer, UserSerializerRead


class CustomerSerializerRead(ModelSerializer):
    sales_contact = UserSerializerRead(many=False)

    class Meta:
        model = Customer
        fields = ["id", "first_name", "last_name", "email",
                  "phone", "mobile", "company_name", "sales_contact"]
        depth = 2


class CustomerSerializerCRUD(ModelSerializer):
    first_name = fields.CharField(required=True, max_length=25)
    last_name = fields.CharField(required=True, max_length=25)
    email = fields.EmailField(required=True, max_length=100)
    phone = fields.CharField(required=True, max_length=25)
    mobile = fields.CharField(required=True, max_length=25)
    company_name = fields.CharField(required=True, max_length=250)
    sales_contact = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Customer
        fields = [
            "first_name", "last_name", "email",
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


class ContractSerializerRead(ModelSerializer):
    customer_assigned = CustomerSerializerRead(many=False)

    class Meta:
        model = Contract
        fields = ['id', 'title', 'date_start_contract',
                  'date_end_contract', 'signed', 'customer_assigned']
        depth = 2


class ContractSerializerCRUD(ModelSerializer):
    title = fields.CharField(required=True, max_length=125)
    #char ou datefield
    date_start_contract = fields.DateField(default=date.today)
    date_end_contract = fields.DateField(required=True)
    signed = fields.BooleanField(default=False)
    customer_assigned = CustomerSerializerRead(many=False, read_only=True)

    class Meta:
        model = Contract
        fields = [
            'title', 'date_start_contract',
            'date_end_contract', 'signed', 'customer_assigned']

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
        contract.mobile = validated_data["mobile"]
        contract.customer_assigned = customer
        contract.save()
        return True

    def delete(self, pk):
        contract = Contract.objects.filter(id=pk).first()
        contract.delete()
        return True
