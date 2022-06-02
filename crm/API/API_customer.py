from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
import re

from authentication.models import User
from crm.API import serializers as srlz

import logging

from crm.models import Customer

logger = logging.getLogger(__name__)


class CustomerViews(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = srlz.CustomerSerializer

    def read_customer(self, request):
        """
        GET Method - Get List of Customers into db
        Return :
            - List of Customers
        """
        serializer = srlz.CustomerSerializer(data=request.data)
        if (
            request.user.profile_staff.customer_read
           ) or (request.user.profile_staff.customer_CRUD_all):
            customers = Customer.objects.all().order_by('id')
            serializer = srlz.CustomerSerializer(customers, many=True)
            logger.info("GET_LIST_CUSTOMERS__202 WITH PROFILE:" +
                        request.user.profile_staff.name)
            return Response(serializer.data,
                            status=status.HTTP_202_ACCEPTED)
        else:
            logger.error(
                "GET_LIST_CUSTOMERS__401 - ERROR profile read customer:" +
                request.user.profile_staff.name)
            return Response({'ERROR profile read customer'},
                            status=status.HTTP_401_UNAUTHORIZED)

    def create_customer(self, request):
        """
        POST Method to create new customer
        Return :
            - details customer
        """
        customer_mail_already_use = (
            Customer.objects.filter(email=request.data.get("email", None))
        ).first()
        if customer_mail_already_use is not None:
            msg = "POST_CREATE_CUSTOMER__406_NOT_ACCEPTABLE " + (
                "Email Customer already Used !")
            logger.error(msg)
            return Response(msg,
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        if request.user.profile_staff.customer_CRUD_all or (
            request.user.profile_staff.customer_CRU_assigned
        ):
            email = request.data.get('sales_contact__email', '')
            user_sales_contact = User.objects.filter(email=email).first()
            if user_sales_contact is not None:
                serializer = srlz.CustomerSerializer(data=request.data)
                if serializer.is_valid():
                    save_ok = serializer.create(
                        serializer.data, user_sales_contact)
                    if save_ok:
                        customer = Customer.objects.all().last()
                        serializer = srlz.CustomerSerializer(customer)
                        logger.info(
                            "POST_CREATE_CUSTOMER__202 - Customer ID_" +
                            str(customer.id) + " with profile : " +
                            request.user.profile_staff.name)
                        return Response(
                            serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    logger.error(
                        "POST_CREATE_CUSTOMER__406_NOT_ACCEPTABLE " +
                        " with profile : " +
                        request.user.profile_staff.name)
                    return Response(
                        serializer.errors,
                        status=status.HTTP_406_NOT_ACCEPTABLE)
            logger.error(
                        "POST_CREATE_CUSTOMER__406 - " +
                        "Error Sales_contact Data " +
                        "with profile : " +
                        request.user.profile_staff.name)
            return Response("Error Sales_contact Data",
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        logger.error(
            "POST_CREATE_CUSTOMER__401 - " +
            "with profile : " +
            request.user.profile_staff.name)
        return Response({'ERROR profile to create contract'},
                        status=status.HTTP_401_UNAUTHORIZED)

    def details_customer(self, request, id_customer):
        """
        GET Method for details project
        Return :
            - details customer ID
        """
        if id_customer == "search":
            id_customer = request.GET.get("id", "")
        logger.info(
                "TRY GET_CUSTOMER_ID_"+str(id_customer))
        get_object_or_404(Customer, id=id_customer)
        customer = Customer.objects.filter(id=id_customer)
        if customer.exists() and (
            request.user.profile_staff.customer_read
           ) or (request.user.profile_staff.customer_CRUD_all):
            serializer = srlz.CustomerSerializer(
                customer.first(), many=False)
            logger.info(
                "GET_CUSTOMER_ID_"+str(id_customer) + '__202 -'
                "with profile : " +
                request.user.profile_staff.name)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            logger.error(
                "GET_CUSTOMER_ID_"+str(id_customer) + '__406 -'
                "with profile : " +
                request.user.profile_staff.name)
            return Response("UNAUTHORIZED for your Profile Staff",
                            status=status.HTTP_401_UNAUTHORIZED)

    def put_customer(self, request, id_customer):
        """
        PUT Method for details project
        Return :
            - details customer
        """
        logger.info("TRY PUT_CUSTOMER_ID_"+str(id_customer))
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
                msg_error = "Error Sales_contact email, you can modify\
                this customer but not sales_contact assigned\
                - see this with your manager !"
                logger.error(
                    "PUT_CUSTOMER_ID_"+str(id_customer)+"__406 : " + msg_error)
                return Response(
                    msg_error,
                    status=status.HTTP_406_NOT_ACCEPTABLE)

            user_sales_contact = User.objects.filter(email=email).first()
            if customer is not None and user_sales_contact is not None:
                serializer = srlz.CustomerSerializer(data=request.data)
                if serializer.is_valid():
                    save_ok = serializer.put(
                        serializer.data, id_customer, user_sales_contact)
                    if save_ok:
                        customer = Customer.objects.filter(
                            id=id_customer).first()
                        serializer = srlz.CustomerSerializer(customer)
                        logger.error(
                            "PUT_CUSTOMER_ID_"+str(id_customer)+"__202")
                        return Response(
                            serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    logger.error(
                        "PUT_CUSTOMER_ID_"+str(id_customer) +
                        "__406_NOT_ACCEPTABLE")
                    return Response(
                        serializer.errors,
                        status=status.HTTP_406_NOT_ACCEPTABLE)
            logger.error(
                "PUT_CUSTOMER_ID_"+str(id_customer)+"__406 : " +
                "Error Sales_contact Data")
            return Response("Error Sales_contact Data",
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        logger.error(
                "PUT_CUSTOMER_ID_"+str(id_customer)+"__401 : " +
                "UNAUTHORIZED for your Profile Staff : " +
                request.user.profile_staff.name)
        return Response("UNAUTHORIZED for your Profile Staff",
                        status=status.HTTP_401_UNAUTHORIZED)

    def delete_customer(self, request, id_customer):
        """
        DELETE Method for details project
        Return :
            - Successfully
        """
        logger.info(
                "TRY DELETE_CUSTOMER_ID_"+str(id_customer)+"__401 : " +
                "UNAUTHORIZED for your Profile Staff : " +
                request.user.profile_staff.name)
        get_object_or_404(Customer, id=id_customer)
        customer = Customer.objects.filter(id=id_customer)
        if customer.exists() and request.user.profile_staff.customer_CRUD_all:
            serializer = srlz.CustomerSerializer(customer)
            serializer.delete(pk=id_customer)
            logger.error(
                "DELETE_CUSTOMER_ID_"+str(id_customer)+"__202 : " +
                "Profile Staff : " +
                request.user.profile_staff.name)
            return Response("Successfully", status=status.HTTP_202_ACCEPTED)
        else:
            logger.error(
                "DELETE_CUSTOMER_ID_"+str(id_customer)+"__401 : " +
                "UNAUTHORIZED for your Profile Staff : " +
                request.user.profile_staff.name)
            return Response("UNAUTHORIZED for your Profile Staff",
                            status=status.HTTP_401_UNAUTHORIZED)

    def search_mail_customer(self, request, mail):
        """
        GET Method - Get Customer by this mail into db
        Reminder : User into db have a UNIQUE mail
        Return :
            - Object Customer
        """
        if request.user.profile_staff.customer_read or (
            request.user.profile_staff.customer_CRU_assigned) or (
                request.user.profile_staff.customer_CRUD_all
        ):
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,5}\b'
            if re.fullmatch(regex, mail):
                customers = Customer.objects.filter(email=mail)
                if customers.exists():
                    serializer = srlz.CustomerSerializer(
                        customers.first(), many=False)
                    logger.info(
                        "SEARCH_CUSTOMER_MAIL__202 -" +
                        "with profile : " +
                        request.user.profile_staff.name)
                    return Response(serializer.data,
                                    status=status.HTTP_202_ACCEPTED)
                logger.info(
                        "SEARCH_CUSTOMER_MAIL__204_NO_CONTENT")
                return Response("No Customer with this mail",
                                status=status.HTTP_204_NO_CONTENT)
            else:
                return Response("Please, thank to write a correct mail format",
                                status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response("UNAUTHORIZED for your Profile Staff",
                            status=status.HTTP_401_UNAUTHORIZED)

    def search_sales_contact_customer(self, request, mail):
        """
        GET Method - Get Customer by sales_contact assigned into db
        Return :
            - Object Customer
        """
        if request.user.profile_staff.customer_read or (
            request.user.profile_staff.customer_CRU_assigned) or (
                request.user.profile_staff.customer_CRUD_all
        ):
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,5}\b'
            if re.fullmatch(regex, mail):
                sales_contact = User.objects.filter(email=mail)
                if sales_contact is not None:
                    if sales_contact.first().profile_staff.name != "SALES":
                        logger.info(
                            "SEARCH_CUSTOMER_Mail_not_profile_SALES__" +
                            "203_NON_AUTHORITATIVE_INFORMATION")
                        return Response(
                            "User Profile_staff is not 'SALES' with this mail",
                            status=(
                                status.HTTP_203_NON_AUTHORITATIVE_INFORMATION))
                customers = Customer.objects.filter(
                    sales_contact__email=mail).order_by('id')
                if customers.exists():
                    serializer = srlz.CustomerSerializer(
                        customers, many=True)
                    logger.info(
                        "SEARCH_CUSTOMER_MAIL__202 -" +
                        "with profile : " +
                        request.user.profile_staff.name)
                    return Response(serializer.data,
                                    status=status.HTTP_202_ACCEPTED)
                logger.info(
                    "SEARCH_CUSTOMER_Sales_contact_with_MAIL__204_NO_CONTENT")
                return Response(
                    "No Sales_contact assigned for Customer with this mail",
                    status=status.HTTP_204_NO_CONTENT)
            else:
                return Response("Please, thank to write a correct mail format",
                                status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response("UNAUTHORIZED for your Profile Staff",
                            status=status.HTTP_401_UNAUTHORIZED)

    def search_name_customer(self, request):
        """
        GET Method - Get Customer by this last_name or first_name into db
        Reminder : User into db with mail UNIQUE
        Return :
            - Object Customer
        """
        if request.user.profile_staff.customer_read or (
            request.user.profile_staff.customer_CRU_assigned) or (
                request.user.profile_staff.customer_CRUD_all
        ):
            last_name = request.GET.get("last_name", None)
            first_name = request.GET.get("first_name", None)
            if last_name is not None or first_name is not None:
                customers = Customer.objects.filter(
                    Q(last_name=last_name) & Q(first_name=first_name)
                ).order_by('id')
                if not customers.exists():
                    logger.info(
                        "SEARCH_CUSTOMER_NAME__NOT_FOUND - L+F")
                    customers = Customer.objects.filter(last_name=last_name)
                if not customers.exists():
                    logger.info(
                        "SEARCH_CUSTOMER_NAME__NOT_FOUND - Last")
                    customers = Customer.objects.filter(first_name=first_name)
                if not customers.exists():
                    logger.info(
                        "SEARCH_CUSTOMER_NAME__406_NOT_FOUND -" +
                        "with profile : " +
                        request.user.profile_staff.name)
                    return Response(
                        "Please verify last_name and/or first_name  input!",
                        status=status.HTTP_406_NOT_ACCEPTABLE)
                serializer = srlz.CustomerSerializer(
                        customers, many=True)
                logger.info(
                    "SEARCH_CUSTOMER_NAME__202 -" +
                    "with profile : " +
                    request.user.profile_staff.name)
                return Response(
                        serializer.data,
                        status=status.HTTP_202_ACCEPTED)
            else:
                logger.info(
                        "SEARCH_CUSTOMER_NAME__406_NOT_FOUND -" +
                        "with profile : " +
                        request.user.profile_staff.name)
                return Response(
                        "Please verify last_name and/or first_name  input!",
                        status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response("UNAUTHORIZED for your Profile Staff",
                            status=status.HTTP_401_UNAUTHORIZED)
