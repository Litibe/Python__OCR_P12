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
        if request.user.profile_staff.customer_CRUD_all:
            customer = Customer.objects.filter(id=id_customer).first()
            email = request.data.get('sales_contact__email', '')
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
        return Response(status=status.HTTP_409_CONFLICT)
