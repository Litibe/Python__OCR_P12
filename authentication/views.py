from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from authentication.serializers import UserSerializer
from authentication.models import ProfileStaff

import logging

logger = logging.getLogger(__name__)


class UserSignUpView(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def create_a_new_user(self, request):
        """
        POST Method - Create new user into db
        Return :
            - user created informations
        """
        serializer = UserSerializer(data=request.data)
        profile = ProfileStaff.objects.filter(
            name=request.data.get('profile_staff', '')).first()
        if serializer.is_valid() and profile:
            serializer.create(request.data)
            logger.info("POST_CREATE_USER__202")
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)
        if not profile:
            logger.error("POST_CREATE_USER__406 - " +
                         "Merci de saisir le Nom de Profil Staff a attribué")
            return Response(
                {'Profile_staff':
                 "Merci de saisir le Nom de Profil Staff a attribué"},
                status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(serializer.errors,
                        status=status.HTTP_406_NOT_ACCEPTABLE)
