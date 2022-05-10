from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from authentication.models import ProfileStaff, User
from crm.models import Contract, Customer
from crm import serializers as srlz


def main_page(request):
    return render(request, "crm/index.html")


class CustomerViews(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = srlz.CustomerSerializerRead

    def read_customer(self, request, format=None):
        """
        GET Method - Get List of Customers into db
        Return :
            - List of Customers
        """
        request.user.profile_staff.customer_read
        serializer = srlz.CustomerSerializerRead(data=request.data)
        if request.user.profile_staff.customer_read:
            customers = Customer.objects.all()
            serializer = srlz.CustomerSerializerRead(customers, many=True)
            return Response(serializer.data,
                            status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'ERROR profile read customer'},
                            status=status.HTTP_401_UNAUTHORIZED)

    def create_customer(self, request):
        """
        POST Method to create new customer
        Return :
            - details customer
        """
        if request.user.profile_staff.customer_CRUD_all or (
            request.user.profile_staff.customer_CRU_assigned
        ):
            email = request.data.get('sales_contact__email', '')
            user_sales_contact = User.objects.filter(email=email).first()
            if user_sales_contact is not None:
                serializer = srlz.CustomerSerializerCRUD(data=request.data)
                if serializer.is_valid():
                    save_ok = serializer.create(
                        serializer.data, user_sales_contact)
                    if save_ok:
                        customer = Customer.objects.all().last()
                        serializer = srlz.CustomerSerializerRead(customer)
                        return Response(
                            serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(
                        serializer.errors,
                        status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response("Error Sales_contact Data",
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(status=status.HTTP_409_CONFLICT)

    def details_customer(self, request, id_customer):
        """
        GET Method for details project
        Return :
            - details customer ID
        """
        get_object_or_404(Customer, id=id_customer)
        customer = Customer.objects.filter(id=id_customer)
        if customer.exists():
            serializer = srlz.CustomerSerializerRead(
                customer.first(), many=False)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def put_customer(self, request, id_customer):
        """
        PUT Method for details project
        Return :
            - details customer
        """
        get_object_or_404(Customer, id=id_customer)
        customer = Customer.objects.filter(id=id_customer).first()
        sales_contact_cru = False
        if customer.sales_contact == request.user:
            if request.user.profile_staff.customer_CRU_assigned and not (
               request.user.profile_staff.customer_CRUD_all):
                sales_contact_cru = True
        if request.user.profile_staff.customer_CRUD_all or sales_contact_cru:
            email = request.data.get('sales_contact__email', '')
            if email != request.user.email and sales_contact_cru is True:
                return Response(
                    "Error Sales_contact email, you can modify this customer\
 but not sales_contact assigned - see this with your manager !",
                    status=status.HTTP_406_NOT_ACCEPTABLE)

            user_sales_contact = User.objects.filter(email=email).first()
            if customer is not None and user_sales_contact is not None:
                serializer = srlz.CustomerSerializerCRUD(data=request.data)
                if serializer.is_valid():
                    save_ok = serializer.put(
                        serializer.data, id_customer, user_sales_contact)
                    if save_ok:
                        customer = Customer.objects.filter(
                            id=id_customer).first()
                        serializer = srlz.CustomerSerializerRead(customer)
                        return Response(
                            serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(
                        serializer.errors,
                        status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response("Error Sales_contact Data",
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response("UNAUTHORIZED for your Profile Staff",
                        status=status.HTTP_401_UNAUTHORIZED)

    def delete_customer(self, request, id_customer):
        """
        DELETE Method for details project
        Return :
            - Boolean
        """
        get_object_or_404(Customer, id=id_customer)
        customer = Customer.objects.filter(id=id_customer)
        if customer.exists() and request.user.profile_staff.customer_CRUD_all:
            serializer = srlz.CustomerSerializerCRUD(customer)
            serializer.delete(pk=id_customer)
            return Response("Successfully", status=status.HTTP_202_ACCEPTED)
        else:
            return Response("UNAUTHORIZED for your Profile Staff",
                            status=status.HTTP_401_UNAUTHORIZED)


class ContractViews(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = srlz.ContractSerializerRead

    def read_contract(self, request, format=None):
        """
        GET Method - Get List of Contract into db
        Return :
            - List of Contract
        """
        serializer = srlz.ContractSerializerRead(data=request.data)
        if request.user.profile_staff.contract_read:
            contracts = Contract.objects.all()
            serializer = srlz.ContractSerializerRead(contracts, many=True)
            return Response(serializer.data,
                            status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'ERROR profile to read contract'},
                            status=status.HTTP_401_UNAUTHORIZED)

    def create_contract(self, request):
        """
        POST Method to create new contract
        Return :
            - details contract
        """
        if request.POST.get("customer_assigned__id", "") != "":
            customer = Customer.objects.filter(
                id=request.POST.get("customer_assigned__id", "")).first()
        else:
            return Response("Error ID Customer assigned",
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        sales_contact_email = customer.sales_contact.email

        if request.user.profile_staff.contract_CRUD_all or (
            request.user.profile_staff.contract_CRU_assigned and (
                request.user.email == sales_contact_email
            )
        ):
            if customer is not None:
                serializer = srlz.ContractSerializerCRUD(data=request.data)
                if serializer.is_valid():
                    save_ok = serializer.create(
                        serializer.data, customer)
                    if save_ok:
                        contract = Contract.objects.all().last()
                        serializer = srlz.ContractSerializerRead(contract)
                        return Response(
                            serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(
                        serializer.errors,
                        status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response("Error Customer_assigned to create new contract",
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def details_contract(self, request, id_contract):
        """
        GET Method for details project
        Return :
            - details customer ID
        """
        get_object_or_404(Contract, id=id_contract)
        contract = Contract.objects.filter(id=id_contract)
        if contract.exists():
            serializer = srlz.ContractSerializerRead(
                contract.first(), many=False)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def put_contract(self, request, id_contract):
        """
        PUT Method to modify a contract by id
        Return :
            - details contract
        """
        get_object_or_404(Contract, id=id_contract)
        contract = Contract.objects.filter(id=id_contract).first()
        if request.POST.get("customer_assigned__id", "") != "":
            customer = Customer.objects.filter(
                id=request.POST.get("customer_assigned__id", "")).first()
        else:
            return Response("Error ID Customer assigned",
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        sales_contact_email = customer.sales_contact.email

        if request.user.profile_staff.contract_CRUD_all or (
            request.user.profile_staff.contract_CRU_assigned and (
                request.user.email == sales_contact_email
            )
        ):
            if customer is not None:
                serializer = srlz.ContractSerializerCRUD(data=request.data)
                if serializer.is_valid():
                    save_ok = serializer.put(
                        serializer.data, pk=id_contract, customer=customer)
                    if save_ok:
                        contract = Contract.objects.filter(
                            id=id_contract).first()
                        serializer = srlz.ContractSerializerRead(contract)
                        return Response(
                            serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(
                        serializer.errors,
                        status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response("Error Customer_assigned to create new contract",
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete_contract(self, request, id_contract):
        """
        DELETE Method to delete a contract
        Return :
            - Boolean
        """
        get_object_or_404(Contract, id=id_contract)
        contract = Contract.objects.filter(id=id_contract)
        if contract.exists() and request.user.profile_staff.contract_CRUD_all:
            serializer = srlz.ContractSerializerCRUD(contract)
            serializer.delete(pk=id_contract)
            return Response("Successfully", status=status.HTTP_202_ACCEPTED)
        else:
            return Response("UNAUTHORIZED for your Profile Staff",
                            status=status.HTTP_401_UNAUTHORIZED)
