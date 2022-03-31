from django.test import Client, TestCase
from django.urls import reverse, resolve

from authentication.models import User, ProfileStaff

def create_profile_staff_support():
    profile_support = ProfileStaff.objects.create(name="SUPPORT")
    profile_support.save()


def create_new_user_support():
    profile_support = ProfileStaff.objects.create(name="SUPPORT")
    profile_support.save()
    profile_staff = ProfileStaff.objects.filter(name="SUPPORT").first()
    new_user = User.objects.create(
        email="support@epicevents.fr",
        first_name="prenom",
        last_name='nom',
        profile_staff=profile_staff,
    )
    new_user.set_password("epicevents")
    new_user.save()


class TestUnitaireAPI(TestCase):
    
    def test_int_create_new_user_error(self):
        client = Client()
        response = client.post(reverse("sign_up"), data={'key1': 'data1',
                                                         'key2': 'data2'})
        assert response.status_code == 406

    def test_int_create_new_user_success(self):
        client = Client()
        create_profile_staff_support()
        response = client.post(reverse("sign_up"),
                               data={'email': 'lioneltissier2@epicevents.fr',
                                     'first_name': 'Lionel2',
                                     'last_name': 'TISSIER2',
                                     'password': 'epicevents',
                                     'profile_staff': 'SUPPORT'})
        assert response.status_code == 201

    def test_int_login_user_success(self):
        create_new_user_support()
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'support@epicevents.fr',
                                     'password': 'epicevents'})
        print(response.data)
        assert response.status_code == 200


class TestUnitaireModels(TestCase):
    def test_models_create_profile_staff(self):
        profile_support = ProfileStaff.objects.create(name="SUPPORT")
        profile_support.save()
        search_profile = ProfileStaff.objects.filter(name="SUPPORT").first()
        assert search_profile.name == "SUPPORT"

    def test_models_create_user(self):
        create_profile_staff_support()
        profile_staff = ProfileStaff.objects.filter(name="SUPPORT").first()
        user = User.objects.create(
            email='lioneltissier2@epicevents.fr',
            first_name='Lionel2',
            last_name='TISSIER2',
            password='epicevents',
            profile_staff=profile_staff)
        user.save()
        search_user = User.objects.filter(
            email='lioneltissier2@epicevents.fr').first()
        assert search_user.email == 'lioneltissier2@epicevents.fr'
        assert search_user.first_name == 'Lionel2'
