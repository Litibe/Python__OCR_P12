from datetime import datetime, timedelta
import re
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from crm.models import Contract, Customer
from crm.API import serializers as srlz

import logging

logger = logging.getLogger(__name__)


class ContractViews(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = srlz.ContractSerializer

    def read_contract(self, request):
        """
        GET Method - Get List of Contract into db
        Return :
            - List of Contract
        """
        serializer = srlz.ContractSerializer(data=request.data)
        if request.user.profile_staff.contract_read or (
            request.user.profile_staff.contract_CRU_assigned
        ) or (request.user.profile_staff.contract_CRUD_all):
            contracts = Contract.objects.all().order_by('id')
            serializer = srlz.ContractSerializer(contracts, many=True)
            logger.info("GET_LIST_CONTRACT__202")
            return Response(serializer.data,
                            status=status.HTTP_202_ACCEPTED)
        else:
            logger.error("GET_LIST_CONTRACT__401 - PROFILE : " +
                         request.user.profile_staff.name)
            return Response({'ERROR profile to read contract'},
                            status=status.HTTP_401_UNAUTHORIZED)

    def create_contract(self, request):
        """
        POST Method to create new contract
        Return :
            - details contract
        """
        logger.info("TRY POST_CREATE_CONTRACT")
        customer = Customer.objects.filter(
                id=request.data.get("customer_assigned__id", "")).first()
        if customer is None:
            logger.error("POST_CREATE_CONTRACT__400 -" +
                         "Error ID Customer assigned " + "PROFILE : " +
                         request.user.profile_staff.name)
            return Response("Error ID Customer assigned",
                            status=status.HTTP_400_BAD_REQUEST)
        sales_contact_email = customer.sales_contact.email
        if request.user.profile_staff.contract_CRUD_all or (
            request.user.profile_staff.contract_CRU_assigned and (
                request.user.email == sales_contact_email
            )
        ):
            serializer = srlz.ContractSerializer(data=request.data)
            if serializer.is_valid():
                save_ok = serializer.create(
                    serializer.data, customer)
                if save_ok:
                    contract = Contract.objects.all().last()
                    serializer = srlz.ContractSerializer(contract)
                    logger.error("POST_CREATE_CONTRACT_ID_" +
                                 str(contract.id) + "__202" +
                                 "PROFILE : " +
                                 request.user.profile_staff.name)
                    return Response(
                        serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                logger.error("POST_CREATE_CONTRACT__406 - NOT ACCEPTABLE")
                return Response(
                    serializer.errors,
                    status=status.HTTP_406_NOT_ACCEPTABLE)
        logger.error("POST_CREATE_CONTRACT__401" +
                     "ERROR profile to create contract" +
                     "PROFILE : " +
                     request.user.profile_staff.name)
        return Response({'ERROR profile to create contract'},
                        status=status.HTTP_401_UNAUTHORIZED)

    def details_contract(self, request, id_contract):
        """
        GET Method for details contract
        Return :
            - details customer ID
        """
        logger.info("TRY GET_CONTRACT_ID" + id_contract)
        get_object_or_404(Contract, id=id_contract)
        contract = Contract.objects.filter(id=id_contract)
        if request.user.profile_staff.contract_read or (
            request.user.profile_staff.contract_CRU_assigned
        ) or (request.user.profile_staff.contract_CRUD_all):
            if contract.exists():
                serializer = srlz.ContractSerializer(
                    contract.first(), many=False)
                logger.info("GET_CONTRACT_ID" + id_contract + "__202 - "
                            "PROFILE : " +
                            request.user.profile_staff.name)
                return Response(
                    serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            logger.info("GET_CONTRACT_ID" + id_contract +
                        "__401 - ERROR profile to read contract"
                        "PROFILE : " +
                        request.user.profile_staff.name)
            return Response(
                {'ERROR profile to read contract'},
                status=status.HTTP_401_UNAUTHORIZED)

    def put_contract(self, request, id_contract):
        """
        PUT Method to modify a contract by id
        Return :
            - details contract
        """
        logger.info("TRY PUT_CONTRACT_ID_" + id_contract)
        get_object_or_404(Contract, id=id_contract)
        contract = Contract.objects.filter(id=id_contract).first()
        customer = Customer.objects.filter(
            id=request.data.get("customer_assigned__id", "0")).first()
        if customer is None:
            logger.error("PUT_CONTRACT_ID_" + id_contract + "__406 : " +
                         "Error ID Customer assigned")
            return Response("Error ID Customer assigned",
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        sales_contact_email = customer.sales_contact.email

        if request.user.profile_staff.contract_CRUD_all or (
            request.user.profile_staff.contract_CRU_assigned and (
                request.user.email == sales_contact_email
            )
        ):
            serializer = srlz.ContractSerializer(data=request.data)
            if serializer.is_valid():
                save_ok = serializer.put(
                    serializer.data, pk=id_contract, customer=customer)
                if save_ok:
                    contract = Contract.objects.filter(
                        id=id_contract).first()
                    serializer = srlz.ContractSerializer(contract)
                    logger.info("PUT_CONTRACT_ID_" + id_contract +
                                "__202 : " +
                                "with PROFILE : " +
                                request.user.profile_staff.name)
                    return Response(
                        serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                logger.error("PUT_CONTRACT_ID_" + id_contract +
                             "__406_NOT_ACCEPTABLE")
                return Response(
                    serializer.errors,
                    status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            logger.info("PUT_CONTRACT_ID_" + id_contract +
                        "__401 : " +
                        " UNAUTHORIZED with PROFILE : " +
                        request.user.profile_staff.name)
            return Response("UNAUTHORIZED for your Profile Staff",
                            status=status.HTTP_401_UNAUTHORIZED)

    def delete_contract(self, request, id_contract):
        """
        DELETE Method to delete a contract
        Return :
            - Successfully
        """
        logger.info("TRY DELETE_CONTRACT_ID_" + id_contract)
        get_object_or_404(Contract, id=id_contract)
        contract = Contract.objects.filter(id=id_contract)
        if contract.exists() and request.user.profile_staff.contract_CRUD_all:
            serializer = srlz.ContractSerializer(contract)
            serializer.delete(pk=id_contract)
            logger.info("DELETE_CONTRACT_ID_" + id_contract + "__202")
            return Response("Successfully", status=status.HTTP_202_ACCEPTED)
        else:
            logger.error("DELETE_CONTRACT_ID_" + id_contract + "__401 - " +
                         "UNAUTHORIZED for your Profile : " +
                         request.user.profile_staff.name)
            return Response("UNAUTHORIZED for your Profile Staff",
                            status=status.HTTP_401_UNAUTHORIZED)

    def search_contract_by_name_customer(self, request):
        """
        GET Method - Get Contract by Customer_name into db
        Return :
            - Object Contract
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
                )
                if not customers.exists():
                    logger.info(
                        "SEARCH_CONTRACT_NAME__NOT_FOUND - L+F")
                    customers = Customer.objects.filter(last_name=last_name)
                    contract = Contract.objects.filter(
                        customer_assigned__last_name=last_name).order_by('id')
                    if not contract.exists():
                        logger.info(
                            "SEARCH_CONTRACT_NAME__NOT_FOUND - Last")
                        contract = Contract.objects.filter(
                            customer_assigned__first_name=first_name
                            ).order_by('id')   
                    if not contract.exists():
                        logger.info(
                            "SEARCH_CONTRACT_NAME__406_NOT_FOUND -" +
                            "with profile : " +
                            request.user.profile_staff.name)
                        return Response(
                            "Please verify last_name and/or first_name input!",
                            status=status.HTTP_406_NOT_ACCEPTABLE)
                else:
                    contract = Contract.objects.filter(
                        customer_assigned=customers.first()).order_by('id')
                serializer = srlz.ContractSerializer(
                        contract, many=True)
                logger.info(
                    "SEARCH_CONTRACT_BY_CUSTOMER_NAME__202 -" +
                    "with profile : " +
                    request.user.profile_staff.name)
                if serializer.data == []:
                    return Response(
                        "Not Contract Found for this Customer: "+(
                            customers.first().id + " " + (
                                customers.first().last_name + " " +
                                customers.first().first_name
                                )),
                        status=status.HTTP_404_NOT_FOUND)
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

    def search_contract_mail_customer(self, request, mail):
        """
        GET Method - Get Contract by email Customer
        Reminder : User into db have a UNIQUE mail
        Return :
            - Object Contract
        """
        if request.user.profile_staff.customer_read or (
            request.user.profile_staff.customer_CRU_assigned) or (
                request.user.profile_staff.customer_CRUD_all
        ):
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,5}\b'
            if re.fullmatch(regex, mail):
                customers = Customer.objects.filter(email=mail)
                if customers.exists():
                    contracts = Contract.objects.filter(
                        customer_assigned=customers.first())
                    serializer = srlz.ContractSerializer(
                        contracts, many=True)
                    logger.info(
                        "SEARCH_CONTRAC_CUSTOMER_MAIL__202 -" +
                        "with profile : " +
                        request.user.profile_staff.name)
                    return Response(serializer.data,
                                    status=status.HTTP_202_ACCEPTED)
                logger.info(
                        "SEARCH_CONTRACT_CUSTOMER_MAIL__204_NO_CONTENT")
                return Response("No Customer with this mail",
                                status=status.HTTP_204_NO_CONTENT)
            else:
                return Response("Please, thank to write a correct mail format",
                                status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response("UNAUTHORIZED for your Profile Staff",
                            status=status.HTTP_401_UNAUTHORIZED)

    def search_contract_by_date_start(self, request, date):
        """
        GET Method - Get Contract by Customer_name into db
        Return :
            - Object Contract
        """
        if request.user.profile_staff.customer_read or (
            request.user.profile_staff.customer_CRU_assigned) or (
                request.user.profile_staff.customer_CRUD_all
        ):
            date_contract = date.split("-")
            contracts = Contract.objects.filter(
                date_start_contract__year=date_contract[0],
                date_start_contract__month=date_contract[1],
                date_start_contract__day=date_contract[2]).order_by("id")
            serializer = srlz.ContractSerializer(contracts, many=True)
            if serializer.data == []:
                return Response(
                    "No Contract Found with date_start_contract : " + (
                        date),
                    status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(serializer.data,
                                status=status.HTTP_202_ACCEPTED)
        else:
            return Response("UNAUTHORIZED for your Profile Staff",
                            status=status.HTTP_401_UNAUTHORIZED)

    def search_contract_by_date_end(self, request, date):
        """
        GET Method - Get Contract by Customer_name into db
        Return :
            - Object Contract
        """
        if request.user.profile_staff.customer_read or (
            request.user.profile_staff.customer_CRU_assigned) or (
                request.user.profile_staff.customer_CRUD_all
        ):
            date_contract = date.split("-")
            contracts = Contract.objects.filter(
                date_end_contract__year=date_contract[0],
                date_end_contract__month=date_contract[1],
                date_end_contract__day=date_contract[2]).order_by("id")
            serializer = srlz.ContractSerializer(contracts, many=True)
            if serializer.data == []:
                return Response(
                    "No Contract Found with date_end_contract : " + (
                        date),
                    status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(serializer.data,
                                status=status.HTTP_202_ACCEPTED)
        else:
            return Response("UNAUTHORIZED for your Profile Staff",
                            status=status.HTTP_401_UNAUTHORIZED)

    def search_contract_by_amount(self, request, amount):
        """
        GET Method - Get Contract by Customer_name into db
        Return :
            - Object Contract
        """
        if request.user.profile_staff.customer_read or (
            request.user.profile_staff.customer_CRU_assigned) or (
                request.user.profile_staff.customer_CRUD_all
        ):
            if "$" not in amount:
                amount += "$"
            contracts = Contract.objects.filter(
                amount=amount).order_by("id")
            serializer = srlz.ContractSerializer(contracts, many=True)
            if serializer.data == []:
                return Response(
                    "No Contract Found with this amount : " + (
                        amount),
                    status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(serializer.data,
                                status=status.HTTP_202_ACCEPTED)
        else:
            return Response("UNAUTHORIZED for your Profile Staff",
                            status=status.HTTP_401_UNAUTHORIZED)
