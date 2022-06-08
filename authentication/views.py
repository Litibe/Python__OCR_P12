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
        if request.user.profile_staff.manage_staff_user_crud:
            profile = ProfileStaff.objects.filter(
                name=request.data.get('profile_staff', None)).first()
            if profile is None:
                logger.error("POST_CREATE_USER__406 - " +
                             "Please input Profile_name")
                return Response(
                    {'Profile_staff':
                     "Merci de saisir le Nom de Profil Staff a attribué"},
                    status=status.HTTP_406_NOT_ACCEPTABLE)
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid() and profile is not None:
                serializer.create(request.data)
                logger.info("POST_CREATE_USER__202")
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({'ERROR profile Manage Staff'},
                        status=status.HTTP_401_UNAUTHORIZED)
