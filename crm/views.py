from datetime import datetime
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from authentication.models import User
from crm.models import Contract, Customer, Event, Need
from crm import serializers as srlz


def main_page(request):
    return render(request, "crm/index.html")


class CustomerViews(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = srlz.CustomerSerializer

    def read_customer(self, request, format=None):
        """
        GET Method - Get List of Customers into db
        Return :
            - List of Customers
        """
        serializer = srlz.CustomerSerializer(data=request.data)
        if (
            request.user.profile_staff.customer_read
           ) or (request.user.profile_staff.customer_CRUD_all):
            customers = Customer.objects.all()
            serializer = srlz.CustomerSerializer(customers, many=True)
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
                serializer = srlz.CustomerSerializer(data=request.data)
                if serializer.is_valid():
                    save_ok = serializer.create(
                        serializer.data, user_sales_contact)
                    if save_ok:
                        customer = Customer.objects.all().last()
                        serializer = srlz.CustomerSerializer(customer)
                        return Response(
                            serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(
                        serializer.errors,
                        status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response("Error Sales_contact Data",
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({'ERROR profile to create contract'},
                        status=status.HTTP_401_UNAUTHORIZED)

    def details_customer(self, request, id_customer):
        """
        GET Method for details project
        Return :
            - details customer ID
        """
        get_object_or_404(Customer, id=id_customer)
        customer = Customer.objects.filter(id=id_customer)
        if customer.exists() and (
            request.user.profile_staff.customer_read
           ) or (request.user.profile_staff.customer_CRUD_all):
            serializer = srlz.CustomerSerializer(
                customer.first(), many=False)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response("UNAUTHORIZED for your Profile Staff",
                            status=status.HTTP_401_UNAUTHORIZED)

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
                serializer = srlz.CustomerSerializer(data=request.data)
                if serializer.is_valid():
                    save_ok = serializer.put(
                        serializer.data, id_customer, user_sales_contact)
                    if save_ok:
                        customer = Customer.objects.filter(
                            id=id_customer).first()
                        serializer = srlz.CustomerSerializer(customer)
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
            - Successfully
        """
        get_object_or_404(Customer, id=id_customer)
        customer = Customer.objects.filter(id=id_customer)
        if customer.exists() and request.user.profile_staff.customer_CRUD_all:
            serializer = srlz.CustomerSerializer(customer)
            serializer.delete(pk=id_customer)
            return Response("Successfully", status=status.HTTP_202_ACCEPTED)
        else:
            return Response("UNAUTHORIZED for your Profile Staff",
                            status=status.HTTP_401_UNAUTHORIZED)


class ContractViews(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = srlz.ContractSerializer

    def read_contract(self, request, format=None):
        """
        GET Method - Get List of Contract into db
        Return :
            - List of Contract
        """
        serializer = srlz.ContractSerializer(data=request.data)
        if request.user.profile_staff.contract_read:
            contracts = Contract.objects.all()
            serializer = srlz.ContractSerializer(contracts, many=True)
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
        if request.data.get("customer_assigned__id", "") != "":
            customer = Customer.objects.filter(
                id=request.data.get("customer_assigned__id", "")).first()
        if customer is None:
            return Response("Error ID Customer assigned",
                            status=status.HTTP_400_BAD_REQUEST)
        sales_contact_email = customer.sales_contact.email
        if request.user.profile_staff.contract_CRUD_all or (
            request.user.profile_staff.contract_CRU_assigned and (
                request.user.email == sales_contact_email
            )
        ):
            if customer is not None:
                serializer = srlz.ContractSerializer(data=request.data)
                if serializer.is_valid():
                    save_ok = serializer.create(
                        serializer.data, customer)
                    if save_ok:
                        contract = Contract.objects.all().last()
                        serializer = srlz.ContractSerializer(contract)
                        return Response(
                            serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(
                        serializer.errors,
                        status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response(
                "Error Sales_contact_assigned to create new contract",
                status=status.HTTP_401_UNAUTHORIZED)
        return Response({'ERROR profile to create contract'},
                        status=status.HTTP_401_UNAUTHORIZED)

    def details_contract(self, request, id_contract):
        """
        GET Method for details contract
        Return :
            - details customer ID
        """
        get_object_or_404(Contract, id=id_contract)
        contract = Contract.objects.filter(id=id_contract)
        if request.user.profile_staff.contract_read:
            if contract.exists():
                serializer = srlz.ContractSerializer(
                    contract.first(), many=False)
                return Response(
                    serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(
                {'ERROR profile to read contract'},
                status=status.HTTP_401_UNAUTHORIZED)

    def put_contract(self, request, id_contract):
        """
        PUT Method to modify a contract by id
        Return :
            - details contract
        """
        get_object_or_404(Contract, id=id_contract)
        contract = Contract.objects.filter(id=id_contract).first()
        if request.data.get("customer_assigned__id", "") != "":
            customer = Customer.objects.filter(
                id=request.data.get("customer_assigned__id", "")).first()
        else:
            return Response("Error ID Customer assigned",
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        if customer is None:
            return Response("Error ID Customer assigned",
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        sales_contact_email = customer.sales_contact.email

        if request.user.profile_staff.contract_CRUD_all or (
            request.user.profile_staff.contract_CRU_assigned and (
                request.user.email == sales_contact_email
            )
        ):
            if customer is not None:
                serializer = srlz.ContractSerializer(data=request.data)
                if serializer.is_valid():
                    save_ok = serializer.put(
                        serializer.data, pk=id_contract, customer=customer)
                    if save_ok:
                        contract = Contract.objects.filter(
                            id=id_contract).first()
                        serializer = srlz.ContractSerializer(contract)
                        return Response(
                            serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(
                        serializer.errors,
                        status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response(
                "Error sales_contact access into customer to modify contract",
                status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response("UNAUTHORIZED for your Profile Staff",
                            status=status.HTTP_401_UNAUTHORIZED)

    def delete_contract(self, request, id_contract):
        """
        DELETE Method to delete a contract
        Return :
            - Successfully
        """
        get_object_or_404(Contract, id=id_contract)
        contract = Contract.objects.filter(id=id_contract)
        if contract.exists() and request.user.profile_staff.contract_CRUD_all:
            serializer = srlz.ContractSerializer(contract)
            serializer.delete(pk=id_contract)
            return Response("Successfully", status=status.HTTP_202_ACCEPTED)
        else:
            return Response("UNAUTHORIZED for your Profile Staff",
                            status=status.HTTP_401_UNAUTHORIZED)


class EventViews(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = srlz.EventSerializer

    def read_event(self, request, format=None):
        """
        GET Method - Get List of Events into db
        Return :
            - List of Events
        """
        request.user.profile_staff.event_read
        serializer = srlz.EventSerializer(data=request.data)
        if request.user.profile_staff.event_read or (
            request.user.profile_staff.event_CRUD_all
        ):
            events = Event.objects.all()
            serializer = srlz.EventSerializer(events, many=True)
            return Response(serializer.data,
                            status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'ERROR profile read events list'},
                            status=status.HTTP_401_UNAUTHORIZED)

    def details_event(self, request, id_event):
        """
        GET Method for details event
        Return :
            - details event ID
        """
        get_object_or_404(Event, id=id_event)
        event = Event.objects.filter(id=id_event)
        if request.user.profile_staff.event_read or (
            request.user.profile_staff.event_CRUD_all
        ):
            if event.exists():
                serializer = srlz.EventSerializer(
                    event.first(), many=False)
                return Response(
                    serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'ERROR profile read event'},
                            status=status.HTTP_401_UNAUTHORIZED)

    def create_event(self, request):
        """
        POST Method to create new event
        Return :
            - details event
        """
        if request.user.profile_staff.event_CRUD_all or (
           request.user.profile_staff.event_CRU_assigned):
            if request.data.get("contract_assigned__id", "") != "":
                contract_assigned = Contract.objects.filter(
                        id=request.data.get(
                            "contract_assigned__id", "")).first()
                if contract_assigned is None:
                    return Response("Error ID Contract assigned",
                                    status=status.HTTP_400_BAD_REQUEST)
                if contract_assigned.date_end_contract < datetime.now():
                    return Response("Error Contract Finished !",
                                    status=status.HTTP_408_REQUEST_TIMEOUT)
            else:
                return Response("Error ID Contract assigned",
                                status=status.HTTP_400_BAD_REQUEST)
            sales_contact_email = (
                    contract_assigned.customer_assigned.sales_contact.email)
            if request.data.get("support_contact__email", "") != "":
                input_email = request.data.get("support_contact__email", "")
                support_contact = User.objects.filter(
                        email=input_email).first()
                if support_contact is None:
                    return Response(
                        "Error Support_contact email assigned not existing",
                        status=status.HTTP_400_BAD_REQUEST)
                if support_contact.profile_staff.id != 3:
                    return Response(
                        "Error Support_contact email havn't a profile SUPPORT",
                        status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Error input Support_contact email assigned",
                                status=status.HTTP_400_BAD_REQUEST)
            if request.user.profile_staff.event_CRUD_all or (
                request.user.profile_staff.event_CRU_assigned and (
                    request.user.email == sales_contact_email
                )
            ):
                if contract_assigned is not None:
                    serializer = srlz.EventSerializer(data=request.data)
                    if serializer.is_valid():
                        save_ok = serializer.create(
                            serializer.data, support_contact,
                            contract_assigned)
                        if save_ok:
                            event = Event.objects.all().last()
                            serializer = srlz.EventSerializer(event)
                            return Response(
                                serializer.data,
                                status=status.HTTP_202_ACCEPTED)
                    else:
                        return Response(
                            serializer.errors,
                            status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return Response({'ERROR profile to create event'},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'ERROR profile to create event'},
                            status=status.HTTP_401_UNAUTHORIZED)

    def put_event(self, request, id_event):
        """
        PUT Method to modify event by ID
        Return :
            - details event
        """
        get_object_or_404(Event, id=id_event)
        event = Event.objects.filter(id=id_event)
        if request.data.get("contract_assigned__id", "") != "":
            contract_assigned = Contract.objects.filter(
                    id=request.data.get("contract_assigned__id", "")).first()
            if contract_assigned is None:
                return Response("Error ID Contract assigned",
                                status=status.HTTP_400_BAD_REQUEST)
            if contract_assigned.date_end_contract < datetime.now():
                return Response("Error Contract Finished !",
                                status=status.HTTP_408_REQUEST_TIMEOUT)
        else:
            return Response("Error ID Contract assigned",
                            status=status.HTTP_400_BAD_REQUEST)
        sales_contact_email = (
                contract_assigned.customer_assigned.sales_contact.email)
        if request.data.get("support_contact__email", "") != "":
            support_contact = User.objects.filter(
                    email=request.data.get(
                        "support_contact__email", "")).first()
            if support_contact is None:
                return Response(
                    "Error Support_contact email assigned not existing",
                    status=status.HTTP_400_BAD_REQUEST)
            if support_contact.profile_staff.id != 3:
                return Response(
                    "Error Support_contact email assigned not profile SUPPORT",
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Error Support_contact email assigned",
                            status=status.HTTP_400_BAD_REQUEST)
        if request.user.profile_staff.event_CRUD_all or (
            request.user.profile_staff.event_CRU_assigned and (
                request.user.email == sales_contact_email
            ) or (request.user.profile_staff.event_CRU_assigned and (
                request.user.email == support_contact.email
            ))
        ):
            if contract_assigned is not None:
                serializer = srlz.EventSerializer(data=request.data)
                if serializer.is_valid():
                    save_ok = serializer.put(
                        serializer.data, id_event,
                        support_contact, contract_assigned)
                    if save_ok:
                        event = Event.objects.filter(id=id_event).first()
                        serializer = srlz.EventSerializer(event)
                        return Response(
                            serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(
                        serializer.errors,
                        status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return Response("Error Support_contact email assigned",
                                status=status.HTTP_400_BAD_REQUEST)
        return Response({'ERROR profile to create event'},
                        status=status.HTTP_401_UNAUTHORIZED)

    def delete_event(self, request, id_event):
        """
        DELETE Method to delete a event
        Return :
            - Successfully
        """
        get_object_or_404(Event, id=id_event)
        event = Event.objects.filter(id=id_event)
        if event.exists() and request.user.profile_staff.event_CRUD_all:
            serializer = srlz.EventSerializer(event)
            serializer.delete(pk=id_event)
            return Response("Successfully", status=status.HTTP_202_ACCEPTED)
        else:
            return Response("UNAUTHORIZED for your Profile Staff",
                            status=status.HTTP_401_UNAUTHORIZED)


class NeedViews(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = srlz.NeedSerializer

    def read_need(self, request, format=None):
        """
        GET Method - Get List of Need into db
        Return :
            - List of Needs
        """
        request.user.profile_staff.need_read
        serializer = srlz.NeedSerializer(data=request.data)
        if request.user.profile_staff.need_read or (
            request.user.profile_staff.need_CRUD_all
        ):
            needs = Need.objects.all()
            serializer = srlz.NeedSerializer(needs, many=True)
            return Response(serializer.data,
                            status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'ERROR profile read need list'},
                            status=status.HTTP_401_UNAUTHORIZED)

    def details_need(self, request, id_need):
        """
        GET Method for details event
        Return :
            - details need ID
        """
        get_object_or_404(Need, id=id_need)
        need = Need.objects.filter(id=id_need)
        if request.user.profile_staff.need_read or (
            request.user.profile_staff.need_CRUD_all
        ):
            if need.exists():
                serializer = srlz.NeedSerializer(
                    need.first(), many=False)
                return Response(
                    serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'ERROR profile read need'},
                            status=status.HTTP_401_UNAUTHORIZED)

    def delete_need(self, request, id_need):
        """
        DELETE Method to delete a need
        Return :
            - Successfully
        """
        get_object_or_404(Need, id=id_need)
        need = Need.objects.filter(id=id_need)
        if need.exists() and request.user.profile_staff.need_CRUD_all:
            serializer = srlz.NeedSerializer(need)
            serializer.delete(pk=id_need)
            return Response("Successfully", status=status.HTTP_202_ACCEPTED)
        else:
            return Response("UNAUTHORIZED for your Profile Staff",
                            status=status.HTTP_401_UNAUTHORIZED)

    def create_need(self, request):
        """
        POST Method to create new need
        Return :
            - details need
        """
        if request.data.get("event_assigned__id", "") != "":
            event_assigned = Event.objects.filter(
                id=request.data.get("event_assigned__id", "")).first()
            if event_assigned is None:
                return Response("Error ID Event assigned",
                                status=status.HTTP_400_BAD_REQUEST)
            if event_assigned.date_finished < datetime.now():
                return Response("Error Event Finished",
                                status=status.HTTP_408_REQUEST_TIMEOUT)
        else:
            return Response("Error ID Event assigned",
                            status=status.HTTP_400_BAD_REQUEST)
        support_contact_email = (
            event_assigned.support_contact.email)
        if request.user.profile_staff.need_CRUD_all or (
            request.user.profile_staff.need_CRU_assigned and (
                request.user.email == support_contact_email
            )
        ):
            if event_assigned is not None:
                serializer = srlz.NeedSerializer(data=request.data)
                if serializer.is_valid():
                    save_ok = serializer.create(
                        serializer.data, event_assigned)
                    if save_ok:
                        need = Need.objects.all().last()
                        serializer = srlz.NeedSerializer(need)
                        return Response(
                            serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(
                        serializer.errors,
                        status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({'ERROR profile to create need'},
                        status=status.HTTP_401_UNAUTHORIZED)

    def put_need(self, request, id_need):
        """
        PUT Method to modify need by ID
        Return :
            - details need
        """
        get_object_or_404(Need, id=id_need)
        if request.data.get("event_assigned__id", "") != "":
            event_assigned = Event.objects.filter(
                id=request.data.get("event_assigned__id", "")).first()
            if event_assigned is None:
                return Response("Error ID Event assigned",
                                status=status.HTTP_400_BAD_REQUEST)
            if event_assigned.date_finished < datetime.now():
                return Response("Error Event Finished",
                                status=status.HTTP_408_REQUEST_TIMEOUT)
        else:
            return Response("Error ID Event assigned",
                            status=status.HTTP_400_BAD_REQUEST)
        support_contact_email = (
            event_assigned.support_contact.email)
        if request.user.profile_staff.need_CRUD_all or (
            request.user.profile_staff.need_CRU_assigned and (
                request.user.email == support_contact_email
            )
        ):
            if event_assigned is not None:
                serializer = srlz.NeedSerializer(data=request.data)
                if serializer.is_valid():
                    save_ok = serializer.put(
                        serializer.data, id_need,
                        event_assigned)
                    if save_ok:
                        need = Need.objects.filter(id=id_need).first()
                        serializer = srlz.NeedSerializer(need)
                        return Response(
                            serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(
                        serializer.errors,
                        status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({'ERROR profile to put need'},
                            status=status.HTTP_401_UNAUTHORIZED)
        return Response({'ERROR profile to put need'},
                        status=status.HTTP_401_UNAUTHORIZED)
