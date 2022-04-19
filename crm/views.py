from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from authentication.models import ProfileStaff, User
from crm.models import Customer

from crm.serializers import CustomerSerialiserCRUD, CustomerSerialiserRead


def main_page(request):
    return render(request, "crm/index.html")


class CustomerViews(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerialiserRead

    def read_customer(self, request, format=None):
        """
        GET Method - Get List of Customers into db function profile_user
        Return :
            - List of Customers
        """
        profile_manage = ProfileStaff.objects.filter(name="MANAGE").first()
        request.user.profile_staff.customer_read
        serializer = CustomerSerialiserRead(data=request.data)
        if request.user.profile_staff.customer_read:
            customers = Customer.objects.all()
            serializer = CustomerSerialiserRead(customers, many=True)
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
                serializer = CustomerSerialiserCRUD(data=request.data)
                if serializer.is_valid():
                    save_ok = serializer.create(
                        serializer.data, user_sales_contact)
                    if save_ok:
                        customer = Customer.objects.all().last()
                        serializer = CustomerSerialiserRead(customer)
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
            serializer = CustomerSerialiserRead(customer.first(), many=False)
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
                serializer = CustomerSerialiserCRUD(data=request.data)
                if serializer.is_valid():
                    save_ok = serializer.put(
                        serializer.data, id_customer, user_sales_contact)
                    if save_ok:
                        customer = Customer.objects.filter(
                            id=id_customer).first()
                        serializer = CustomerSerialiserRead(customer)
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
            serializer = CustomerSerialiserCRUD(customer)
            serializer.delete(pk=id_customer)
            return Response("Successfully", status=status.HTTP_202_ACCEPTED)
        else:
            return Response("UNAUTHORIZED for your Profile Staff",
                            status=status.HTTP_401_UNAUTHORIZED)
