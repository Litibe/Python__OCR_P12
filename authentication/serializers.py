from rest_framework.serializers import ModelSerializer, EmailField, CharField
from rest_framework.validators import UniqueValidator
from rest_framework import fields
from django.contrib.auth.password_validation import validate_password

from authentication.models import User, ProfileStaff


class ProfileStaffSerializer(ModelSerializer):
    name = fields.CharField(required=True)

    class Meta:
        model = ProfileStaff
        fields = ('name')


class UserSerializer(ModelSerializer):
    email = EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = CharField(write_only=True, required=True,
                         validators=[validate_password])
    profile_staff = ProfileStaffSerializer(
        read_only=True,
        error_messages={
            'required': "Merci de saisir l'ID de Profil Staff a attribué"})

    class Meta:
        model = User
        fields = ('email', 'password',
                  'last_name', 'first_name', 'profile_staff', 'id')

    def create(self, validated_data):
        profile = ProfileStaff.objects.filter(
            name=validated_data['profile_staff']).first()
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            profile_staff=profile,
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializerRead(ModelSerializer):
    class Meta:
        model = User
        fields = ('email',
                  'last_name', 'first_name', 'profile_staff')


class UserSerializerPut(ModelSerializer):
    class Meta:
        model = User
        fields = ('email')
