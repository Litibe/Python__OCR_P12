from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from authentication.models import User
from crm.models import Contract, Event
from crm.API import serializers as srlz

import logging

logger = logging.getLogger(__name__)


class EventViews(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = srlz.EventSerializer

    def read_event(self, request):
        """
        GET Method - Get List of Events into db
        Return :
            - List of Events
        """
        serializer = srlz.EventSerializer(data=request.data)
        if request.user.profile_staff.event_read or (
            request.user.profile_staff.event_CRUD_all
        ):
            events = Event.objects.all()
            serializer = srlz.EventSerializer(events, many=True)
            logger.info("GET_LIST_EVENTS__202")
            return Response(serializer.data,
                            status=status.HTTP_202_ACCEPTED)
        else:
            logger.error("GET_LIST_EVENTS__401 - UNAUTHORIZED PROFILE : " +
                         request.user.profile_staff.name)
            return Response({'ERROR profile read events list'},
                            status=status.HTTP_401_UNAUTHORIZED)

    def details_event(self, request, id_event):
        """
        GET Method for details event
        Return :
            - details event ID
        """
        logger.info("TRY GET_EVENT_ID_" + id_event)
        get_object_or_404(Event, id=id_event)
        event = Event.objects.filter(id=id_event)
        if request.user.profile_staff.event_read or (
            request.user.profile_staff.event_CRUD_all
        ):
            if event.exists():
                serializer = srlz.EventSerializer(
                    event.first(), many=False)
                logger.info("GET_EVENT_ID_" + id_event + "__202")
                return Response(
                    serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            logger.error("GET_EVENT_ID_" + id_event +
                         "__401 - UNAUTHORIZED PROFILE : " +
                         request.user.profile_staff.name)
            return Response({'ERROR profile read event'},
                            status=status.HTTP_401_UNAUTHORIZED)

    def create_event(self, request):
        """
        POST Method to create new event
        Return :
            - details event
        """
        contract_assigned = Contract.objects.filter(
            id=request.data.get(
                "contract_assigned__id", "0")).first()
        if contract_assigned is None:
            logger.error("POST_CREATE_EVENT"
                         "__400 - " +
                         "Error ID Contract assigned")
            return Response("Error ID Contract assigned",
                            status=status.HTTP_400_BAD_REQUEST)
        if contract_assigned.date_end_contract < datetime.now():
            logger.error("POST_CREATE_EVENT"
                         "__400 - " +
                         "Error Contract Finished !" +
                         contract_assigned.id)
            return Response("Error Contract Finished !",
                            status=status.HTTP_408_REQUEST_TIMEOUT)
        if not contract_assigned.signed:
            logger.error("POST_CREATE_EVENT"
                         "__400 - " +
                         "Error Contract not signed !" +
                         contract_assigned.id)
            return Response("Error Contract not signed !",
                            status=status.HTTP_400_BAD_REQUEST)

        sales_contact_email = (
            contract_assigned.customer_assigned.sales_contact.email)
        input_email = request.data.get("support_contact__email", "")
        support_contact = User.objects.filter(
                email=input_email).first()
        if support_contact is None:
            logger.error("POST_CREATE_EVENT"
                         "__400 - Error Support_contact" +
                         " email assigned not existing")
            return Response(
                "Error Support_contact email assigned not existing",
                status=status.HTTP_400_BAD_REQUEST)
        if support_contact.profile_staff.id != 3:
            logger.error("POST_CREATE_EVENT"
                         "__400 - Error Support_contact" +
                         " email havn't a profile SUPPORT")
            return Response(
                "Error Support_contact email havn't a profile SUPPORT",
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
                        logger.info("POST_CREATE_EVENT"
                                    "__202 - " + event.id)
                        return Response(
                            serializer.data,
                            status=status.HTTP_202_ACCEPTED)
                else:
                    logger.error("POST_CREATE_EVENT"
                                 "__406 - ", serializer.errors)
                    return Response(
                        serializer.errors,
                        status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            logger.error("POST_CREATE_EVENT"
                         "__401 - " +
                         "ERROR profile to create event : " +
                         request.user.profile_staff.name)
            return Response({'ERROR profile to create event'},
                            status=status.HTTP_401_UNAUTHORIZED)

    def put_event(self, request, id_event):
        """
        PUT Method to modify event by ID
        Return :
            - details event
        """
        logger.info("TRY PUT_EVENT_ID_" + id_event)
        get_object_or_404(Event, id=id_event)
        event = Event.objects.filter(id=id_event)
        if request.data.get("contract_assigned__id", "") != "":
            contract_assigned = Contract.objects.filter(
                    id=request.data.get("contract_assigned__id", "")).first()
            if contract_assigned is None:
                logger.error("PUT_EVENT_ID_" + id_event +
                             "__400 - " + "Error ID Contract assigned")
                return Response("Error ID Contract assigned",
                                status=status.HTTP_400_BAD_REQUEST)
            if contract_assigned.date_end_contract < datetime.now():
                logger.error("PUT_EVENT_ID_" + id_event +
                             "__400 - " + "Error Contract Finished :" +
                             contract_assigned.id + " : " + str(
                                contract_assigned.date_end_contract))
                return Response("Error Contract Finished !",
                                status=status.HTTP_408_REQUEST_TIMEOUT)
            if not contract_assigned.signed:
                logger.error("PUT_EVENT_ID_" + id_event +
                             "__400 - " + "Error Contract not signed ! :" +
                             contract_assigned.id)
                return Response("Error Contract not signed !",
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.info("PUT_EVENT_ID_" + id_event +
                        "__400 - " + "Error Contract not signed ! :" +
                        contract_assigned.id)
            return Response("Error ID Contract assigned",
                            status=status.HTTP_400_BAD_REQUEST)
        sales_contact_email = (
                contract_assigned.customer_assigned.sales_contact.email)
        if request.data.get("support_contact__email", "") != "":
            support_contact = User.objects.filter(
                    email=request.data.get(
                        "support_contact__email", "")).first()
            if support_contact is None:
                logger.info("PUT_EVENT_ID_" + id_event +
                            "__400 - " + "Error Contract not signed ! :" +
                            contract_assigned.id)
                return Response(
                    "Error Support_contact email assigned not existing",
                    status=status.HTTP_400_BAD_REQUEST)
            if support_contact.profile_staff.id != 3:
                logger.error("PUT_EVENT_ID_" + id_event +
                             "__400 - Error Support_contact" +
                             " email assigned not profile SUPPORT : " +
                             support_contact.profile_staff.name +
                             contract_assigned.id)
                return Response(
                    "Error Support_contact email assigned not profile SUPPORT",
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.error("PUT_EVENT_ID_" + id_event +
                         "__400 - Error Support_contact" +
                         " email assigned" +
                         contract_assigned.id)
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
                        logger.error("PUT_EVENT_ID_" + id_event +
                                     "__202 : " + event.id)
                        return Response(
                            serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    logger.error("PUT_EVENT_ID_" + id_event +
                                 "__406 - ", serializer.errors)
                    return Response(
                        serializer.errors,
                        status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                logger.error("PUT_EVENT_ID_" + id_event +
                             "__400 - " +
                             "Error Support_contact email assigned")
                return Response("Error Support_contact email assigned",
                                status=status.HTTP_400_BAD_REQUEST)
        logger.error("PUT_EVENT_ID_" + id_event +
                     "__401 - ERROR profile to create event" +
                     request.user.profile_staff.name)
        return Response({'ERROR profile to create event'},
                        status=status.HTTP_401_UNAUTHORIZED)

    def delete_event(self, request, id_event):
        """
        DELETE Method to delete a event
        Return :
            - Successfully
        """
        logger.info("TRY DELETE_EVENT_ID_" + id_event)
        get_object_or_404(Event, id=id_event)
        event = Event.objects.filter(id=id_event)
        if event.exists() and request.user.profile_staff.event_CRUD_all:
            serializer = srlz.EventSerializer(event)
            serializer.delete(pk=id_event)
            logger.info("DELETE_EVENT_ID_" + id_event + "__202")
            return Response("Successfully", status=status.HTTP_202_ACCEPTED)
        else:
            logger.info("DELETE_EVENT_ID_" + id_event +
                        "__401 - UNAUTHORIZED Profile : "
                        + request.user.profile_staff.name)
            return Response("UNAUTHORIZED for your Profile Staff",
                            status=status.HTTP_401_UNAUTHORIZED)