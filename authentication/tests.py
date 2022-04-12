from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.admin.sites import AdminSite

from authentication.models import User, ProfileStaff
from authentication.admin import UserAdmin


def create_profile_staff_support():
    profile_support = ProfileStaff.objects.create(name="SUPPORT")
    profile_support.save()


def create_new_user_support():
    profile_support = ProfileStaff.objects.create(
        name="SUPPORT",
        customer_read=True,
        contract_read=True,
        event_read=True,
        event_CRU_assigned=True,
        need_read=True,
        need_CRU_assigned=True,
        )
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


def create_new_user_manage():
    profile_manage = ProfileStaff.objects.create(
        name="MANAGE",
        manage_staff_user_crud=True,
        customer_read=True,
        customer_CRU_assigned=True,
        customer_CRUD_all=True,
        contract_read=True,
        contract_CRU_assigned=True,
        contract_CRUD_all=True,
        event_read=True,
        event_CRU_assigned=True,
        event_CRUD_all=True,
        need_read=True,
        need_CRU_assigned=True,
        need_CRUD_all=True
        )
    profile_manage.save()
    profile_staff = ProfileStaff.objects.filter(name="MANAGE").first()
    new_user = User.objects.create(
        email="manage@epicevents.fr",
        first_name="prenom",
        last_name='nom',
        profile_staff=profile_staff,
    )
    new_user.set_password("epicevents")
    new_user.save()


def create_new_user_sales():
    profile_manage = ProfileStaff.objects.create(
        name="SALES",
        customer_read=True,
        customer_CRU_assigned=True,
        contract_read=True,
        contract_CRU_assigned=True,
        event_read=True,
        event_CRU_assigned=True,
        need_read=True,
    )
    profile_manage.save()
    profile_staff = ProfileStaff.objects.filter(name="SALES").first()
    new_user = User.objects.create(
        email="sales@epicevents.fr",
        first_name="prenom",
        last_name='nom',
        profile_staff=profile_staff,
    )
    new_user.set_password("epicevents")
    new_user.save()

def create_new_users():
    create_new_user_manage()
    create_new_user_sales()
    create_new_user_support()


class TestUnitaireAPI(TestCase):
    @classmethod
    def setup_class(cls):
        create_new_users()
        print("--> Setup Users")

    def test_000_login_user_success_support(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'support@epicevents.fr',
                                     'password': 'epicevents'})
        self.token_user_support = response.get("access")
        assert response.status_code == 200

    def test_001_login_user_success_manage(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        self.token_user_manage = response.get("access")
        assert response.status_code == 200

    def test_002_create_new_user_error_without_loggin(self):
        client = Client()
        response = client.post(reverse("sign_up"), data={'key1': 'data1',
                                                         'key2': 'data2'})
        assert response.status_code == 401

    def test_003_create_new_user_success_with_login(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.post(
            reverse("sign_up"),
            data={'email': 'lioneltissier2@epicevents.fr',
                  'first_name': 'Lionel2',
                  'last_name': 'TISSIER2',
                  'password': 'epicevents',
                  'profile_staff': 'SUPPORT'})
        assert response.status_code == 201


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


class OurRequests(object):
    def __init__(self, user):
        self.user = user


class TestUnitaireModelsAdminAccess(TestCase):

    def SetUp(self):
        create_new_user_manage_support()
        print("--> Setup Users")

    def test_permission_user_manage(
            self, profile_staff=1,
            bol_ad=True, bol_module=True, bol_change=True, bol_del=True):
        self.user_model_admin = UserAdmin(model=User, admin_site=AdminSite())
        user_profil = User.objects.filter(profile_staff=profile_staff).first()
        my_request = OurRequests(user_profil)
        self.assertEqual(
            self.user_model_admin.has_add_permission(
                my_request), bol_ad)
        self.assertEqual(
            self.user_model_admin.has_module_permission(
                my_request), bol_module)
        self.assertEqual(
            self.user_model_admin.has_change_permission(
                my_request), bol_change)
        self.assertEqual(
            self.user_model_admin.has_delete_permission(
                my_request), bol_del)

    def test_permission_user_sales(
            self, profile_staff=2,
            bol_ad=False, bol_module=False, bol_change=False, bol_del=False):
        self.user_model_admin = UserAdmin(model=User, admin_site=AdminSite())
        user_profil = User.objects.filter(profile_staff=profile_staff).first()
        my_request = OurRequests(user_profil)
        self.assertEqual(
            self.user_model_admin.has_add_permission(
                my_request), bol_ad)
        self.assertEqual(
            self.user_model_admin.has_module_permission(
                my_request), bol_module)
        self.assertEqual(
            self.user_model_admin.has_change_permission(
                my_request), bol_change)
        self.assertEqual(
            self.user_model_admin.has_delete_permission(
                my_request), bol_del)

    def test_permission_user_support(
            self, profile_staff=3,
            bol_ad=False, bol_module=False, bol_change=False, bol_del=False):
        self.user_model_admin = UserAdmin(model=User, admin_site=AdminSite())
        user_profil = User.objects.filter(profile_staff=profile_staff).first()
        my_request = OurRequests(user_profil)
        self.assertEqual(
            self.user_model_admin.has_add_permission(
                my_request), bol_ad)
        self.assertEqual(
            self.user_model_admin.has_module_permission(
                my_request), bol_module)
        self.assertEqual(
            self.user_model_admin.has_change_permission(
                my_request), bol_change)
        self.assertEqual(
            self.user_model_admin.has_delete_permission(
                my_request), bol_del)