from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from authentication.models import ProfileStaff
from crm.models import Customer

from crm.serializers import CustomerSerialiser


class CustomerViews(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerialiser

    def read_customer(self, request, format=None):
        """
        GET Method - Get List of Customers into db function profile_user
        Return :
            - List of Customers
        """
        profile_manage = ProfileStaff.objects.filter(name="MANAGE").first()
        request.user.profile_staff.customer_read
        serializer = CustomerSerialiser(data=request.data)
        if request.user.profile_staff.customer_read and (
            request.user.profile_staff == profile_manage):
                customers = Customer.objects.all()
                serializer = CustomerSerialiser(customers, many=True)
                return Response(serializer.data,
                                status=status.HTTP_202_ACCEPTED)
        elif request.user.profile_staff.customer_read:
            customers = Customer.objects.filter(
                sales_contact=request.user
            )
            serializer = CustomerSerialiser(customers, many=True)
            return Response(serializer.data,
                            status=status.HTTP_206_PARTIAL_CONTENT)
        else:
            return Response({'ERROR profile read customer'},
                            status=status.HTTP_401_UNAUTHORIZED)
