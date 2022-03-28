from rest_framework.serializers import ModelSerializer, EmailField, CharField
from rest_framework.validators import UniqueValidator
from rest_framework import fields
from django.contrib.auth.password_validation import validate_password

from authentication.models import User


class UserSerializer(ModelSerializer):
    email = EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = CharField(write_only=True, required=True,
                         validators=[validate_password])
    profile = fields.ChoiceField(choices=User.profile_choices.choices)

    class Meta:
        model = User
        fields = ('email', 'password',
                  'last_name', 'first_name', 'profile', 'id')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'profile': {'required': True},
        }

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            profile=validated_data['profile']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
