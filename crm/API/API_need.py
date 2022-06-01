from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from crm.models import Event, Need
from crm.API import serializers as srlz

import logging

logger = logging.getLogger(__name__)


class NeedViews(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = srlz.NeedSerializer

    def read_need(self, request):
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
            logger.info("GET_LIST_NEED__202")
            return Response(serializer.data,
                            status=status.HTTP_202_ACCEPTED)
        else:
            logger.error("GET_LIST_NEED__401 - UNAUTHORIZED PROFILE : " +
                         request.user.profile_staff.name)
            return Response({'ERROR profile read need list'},
                            status=status.HTTP_401_UNAUTHORIZED)

    def details_need(self, request, id_need):
        """
        GET Method for details event
        Return :
            - details need ID
        """
        logger.info("TRY GET_NEED_ID_" + id_need)
        get_object_or_404(Need, id=id_need)
        need = Need.objects.filter(id=id_need)
        if request.user.profile_staff.need_read or (
            request.user.profile_staff.need_CRUD_all
        ):
            if need.exists():
                serializer = srlz.NeedSerializer(
                    need.first(), many=False)
                logger.info("GET_NEED_ID_" + id_need + "__202")
                return Response(
                    serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            logger.error("GET_NEED_ID_" + id_need +
                         "__401 : UNAUTHORIZED PROFILE : " +
                         request.user.profile_staff.name)
            return Response({'ERROR profile read need'},
                            status=status.HTTP_401_UNAUTHORIZED)

    def delete_need(self, request, id_need):
        """
        DELETE Method to delete a need
        Return :
            - Successfully
        """
        logger.info("TRY DELETE_NEED_ID_"+id_need)
        get_object_or_404(Need, id=id_need)
        need = Need.objects.filter(id=id_need)
        if need.exists() and request.user.profile_staff.need_CRUD_all:
            serializer = srlz.NeedSerializer(need)
            serializer.delete(pk=id_need)
            logger.info("DELETE_NEED_ID_" + id_need + "__202")
            return Response("Successfully", status=status.HTTP_202_ACCEPTED)
        else:
            logger.error("DELETE_NEED_ID_" + id_need + '__401 - ' +
                         "UNAUTHORIZED PROFILE : " +
                         request.user.profile_staff.name)
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
                logger.error("POST_CREATE_NEED_400 - Error ID" +
                             " Event assigned " +
                             request.data.get("event_assigned__id", ""))
                return Response("Error ID Event assigned",
                                status=status.HTTP_400_BAD_REQUEST)
            if event_assigned.date_finished < datetime.now():
                logger.error("POST_CREATE_NEED_408 - Error Event Finished : " +
                             event_assigned.id + " - " +
                             event_assigned.date_finished)
                return Response("Error Event Finished",
                                status=status.HTTP_408_REQUEST_TIMEOUT)
        else:
            logger.error("POST_CREATE_NEED_400 - Error ID Event assigned : " +
                         request.data.get("event_assigned__id", ""))
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
                        logger.info("POST_CREATE_NEED__202 - " + need.id)
                        return Response(
                            serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    logger.error("POST_CREATE_NEED__406 - ",
                                 serializer.errors)
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
        logger.info("TRY PUT_NEED_ID_" + id_need)
        get_object_or_404(Need, id=id_need)
        if request.data.get("event_assigned__id", "") != "":
            event_assigned = Event.objects.filter(
                id=request.data.get("event_assigned__id", "")).first()
            if event_assigned is None:
                logger.error("PUT_NEED_ID_" + id_need + "__400 - " +
                             "Error ID Event assigned : " +
                             request.data.get("event_assigned__id", ""))
                return Response("Error ID Event assigned",
                                status=status.HTTP_400_BAD_REQUEST)
            if event_assigned.date_finished < datetime.now():
                logger.error("PUT_NEED_ID_" + id_need + "__400 - " +
                             "Error Event Finished : " +
                             event_assigned.id + " : " +
                             event_assigned.date_finished)
                return Response("Error Event Finished",
                                status=status.HTTP_408_REQUEST_TIMEOUT)
        else:
            logger.error("PUT_NEED_ID_" + id_need + "__400 - " +
                         "Error ID Event assigned : " +
                         request.data.get("event_assigned__id", ""))
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
                        logger.info("PUT_NEED_ID_" + id_need + "__202")
                        return Response(
                            serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    logger.error("PUT_NEED_ID_" + id_need + "__406 - ",
                                 serializer.errors)
                    return Response(
                        serializer.errors,
                        status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            logger.error("PUT_NEED_ID_" + id_need + "__406 - " +
                         'ERROR profile to put need')
            return Response({'ERROR profile to put need'},
                            status=status.HTTP_401_UNAUTHORIZED)
        logger.error("PUT_NEED_ID_" + id_need + "__401 - " +
                     'UNAUTHORIED PROFILE : ' +
                     request.user.profile_staff.name)
        return Response({'ERROR profile to put need'},
                        status=status.HTTP_401_UNAUTHORIZED)
