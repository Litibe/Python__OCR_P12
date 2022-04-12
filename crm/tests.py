from parameterized import parameterized
from django.test import TestCase
from django.contrib.admin.sites import AdminSite
import pytest

from authentication.models import ProfileStaff, User
from authentication.tests import create_new_users
from crm.admin import CustomerAdmin, ContractAdmin, EventAdmin, NeedAdmin
from crm.models import Contract, Customer, Event, Need


def create_C_C_E_N():
    profile_staff = ProfileStaff.objects.filter(name="SALES").first()
    user_sales = User.objects.filter(
            profile_staff=profile_staff).first()
    profile_staff = ProfileStaff.objects.filter(name="SUPPORT").first()
    user_support = User.objects.filter(
            profile_staff=profile_staff).first()
    db_customer = create_new_customer(user_sales)
    print(db_customer)
    db_contract = create_new_contract(db_customer)
    print(db_contract)
    db_event = create_new_event(db_contract, user_support)
    print(db_event)
    db_need = create_new_need(db_event)
    print(db_need)


def create_new_customer(user_sales):
    """Create New Customer into DB TEST

    Args:
        user_sales (User Object with Profile_staff.id=2)

    Returns:
        Customer Object created after search into db
    """
    new_customer = Customer.objects.create(
            first_name="Tony",
            last_name="DURAND",
            email="tonydurant@entreprise.com",
            phone="0987654321",
            mobile="067899887",
            company_name="Entreprise SAS",
            sales_contact=user_sales
        )
    new_customer.save()
    search_customer = Customer.objects.all().first()
    return search_customer


def create_new_contract(search_customer):
    """Create New Contract into DB TEST

    Args:
        search_customer (Customer Object)

    Returns:
        Contract Object created after search into db
    """
    d_start = "2022-06-03T08:00:00+02:00"
    d_end = "2022-06-05T20:00:00+02:00"
    new_contract = Contract.objects.create(
        title="Spring 2022 - Paris",
        date_start_contract=d_start,
        date_end_contract=d_end,
        signed=True,
        customer_assigned=search_customer
    )
    new_contract.save()
    search_contract = Contract.objects.filter(
                        title="Spring 2022 - Paris").first()
    return search_contract


def create_new_event(search_contract, user_contact):
    """Create New Event into DB TEST

    Args:
        search_contract (Contract Object)
        user_contact (USer Object - profile_staff.name=="SUPPORT")

    Returns:
        Event Object created after search into db
    """
    d_start = "2022-06-03T08:00:00+02:00"
    d_end = "2022-06-03T11:00:00+02:00"
    new_event = Event.objects.create(
        title="ROOM 21 into Faculty - Morning",
        date_started=d_start,
        date_finished=d_end,
        support_contact=user_contact,
        contract_assigned=search_contract
    )
    new_event.save()
    search_event = Event.objects.filter(
                        title="ROOM 21 into Faculty - Morning").first()
    return search_event


def create_new_need(search_event):
    """Create New Need into DB TEST

    Args:
        search_event (Event Object)

    Returns:
        Need Object created after search into db
    """
    new_need = Need.objects.create(
        title="Computer and videoprojector",
        event_assigned=search_event
    )
    new_need.save()
    search_need = Need.objects.all().first()
    return search_need


class TestUnitaireModels(TestCase):
    """ Class TEST Unitaire for Models CRM """
    def test_01_create_new_customer(self):
        """create new user_sales into db and new customer with sales_contact
        """
        profile_staff = ProfileStaff.objects.filter(name="SALES").first()
        user_sales = User.objects.filter(
            profile_staff=profile_staff).first()
        db_customer = create_new_customer(user_sales)
        assert db_customer.id == "CM00001"
        assert db_customer.first_name == "Tony"
        assert db_customer.sales_contact.profile_staff.name == "SALES"
        print(db_customer)

    def test_02_create_new_contract(self):
        """create new contract for a customer
        """
        profile_staff = ProfileStaff.objects.filter(name="SALES").first()
        user_sales = User.objects.filter(
            profile_staff=profile_staff).first()
        db_customer = create_new_customer(user_sales)
        print(db_customer)
        db_contract = create_new_contract(db_customer)
        assert db_contract.customer_assigned == db_customer
        assert db_contract.id == "CT00001"
        print(db_contract)

    def test_03_create_new_event(self):
        """create new event for a contract
        """
        profile_staff = ProfileStaff.objects.filter(name="SALES").first()
        user_sales = User.objects.filter(
            profile_staff=profile_staff).first()
        profile_staff = ProfileStaff.objects.filter(name="SUPPORT").first()
        user_support = User.objects.filter(
            profile_staff=profile_staff).first()
        db_customer = create_new_customer(user_sales)
        print(db_customer)
        db_contract = create_new_contract(db_customer)
        print(db_contract)
        db_event = create_new_event(db_contract, user_support)
        print(db_event)

    def test_04_create_new_need(self):
        """create new need for a event
        """
        create_C_C_E_N()


class OurRequests(object):
    def __init__(self, user):
        self.user = user


class TestUnitaireModelsAdminAccess(TestCase):
    @classmethod
    def setup_class(cls):
        create_C_C_E_N()
        """Create another user Sales"""
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
            email="sales2@epicevents.fr",
            first_name="prenom2",
            last_name='nom2',
            profile_staff=profile_staff,
        )
        new_user.set_password("epicevents")
        new_user.save()
        print("--> Setup C.C.E.N")

    @parameterized.expand([
            ["MANAGE", 0, True, True, True, True, True],
            ["SALES", 0, True, True, True, True, False],
            ["SALES", 1, True, True, True, False, False],
            ["SUPPORT", 0, False, True, True, False, False]
            ])
    def test_permission_customer(
            self, profile_staff, user_id,
            bol_ad, bol_view, bol_module, bol_change, bol_del):
        """
        Test Permission differents user into db, 2 user sales differents 
        only first autorized to update Customer Object
        """
        self.user_model_admin = CustomerAdmin(
            model=User, admin_site=AdminSite())
        user_profil = User.objects.filter(
            profile_staff__name=profile_staff)[user_id]
        my_request = OurRequests(user_profil)
        self.assertEqual(
            self.user_model_admin.has_add_permission(
                my_request), bol_ad)
        self.assertEqual(
            self.user_model_admin.has_view_permission(
                my_request), bol_view)
        self.assertEqual(
            self.user_model_admin.has_module_permission(
                my_request), bol_module)
        obj = Customer.objects.all().first()
        self.assertEqual(
            self.user_model_admin.has_change_permission(
                my_request, obj), bol_change)
        self.assertEqual(
            self.user_model_admin.has_delete_permission(
                my_request), bol_del)
