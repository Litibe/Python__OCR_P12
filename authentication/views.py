from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from authentication.serializers import UserSerializer
from authentication.models import ProfileStaff


class UserSignUpView(ViewSet):
    serializer_class = UserSerializer

    def create_a_new_user(self, request, format=None):
        """
        POST Method - Create new user into db
        Return :
            - user created informations
        """
        serializer = UserSerializer(data=request.data)
        profile = ProfileStaff.objects.filter(name=request.data.get('profile_staff', '')).first()
        print(profile)
        if serializer.is_valid() and profile:
            serializer.create(request.data)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        if not profile : 
            return Response({'Profile_staff': "Merci de saisir le Nom de Profil Staff a attribué"},
                        status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(serializer.errors,
                        status=status.HTTP_406_NOT_ACCEPTABLE)
