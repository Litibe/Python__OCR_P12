import datetime
from django.test import TestCase
from authentication.models import ProfileStaff, User

from crm.models import Contract, Customer, Event, Need


def create_new_user_support():
    """Create New User with profile_staff.name==SUPPORT into DB TEST

    Returns:
        User Object with Profile_staff.id=3 created after search into db
    """
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
    user_support = User.objects.filter(profile_staff=profile_staff).first()
    return user_support


def create_new_user_sales():
    """Create New User with profile_staff.name==SALES into DB TEST

    Returns:
        User Object with Profile_staff.id=2 created after search into db
    """
    profile_sales = ProfileStaff.objects.create(name="SALES")
    profile_sales.save()
    profile_staff = ProfileStaff.objects.filter(name="SALES").first()
    new_user = User.objects.create(
        email="sales@epicevents.fr",
        first_name="prenom",
        last_name='nom',
        profile_staff=profile_staff,
    )
    new_user.set_password("epicevents")
    new_user.save()
    user_sales = User.objects.filter(
            profile_staff=profile_staff).first()
    return user_sales


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
        user_sales = create_new_user_sales()
        db_customer = create_new_customer(user_sales)
        assert db_customer.id == "CM00001"
        assert db_customer.first_name == "Tony"
        assert db_customer.sales_contact.profile_staff.name == "SALES"
        print(db_customer)

    def test_02_create_new_contract(self):
        """create new contract for a customer
        """
        user_sales = create_new_user_sales()
        db_customer = create_new_customer(user_sales)
        print(db_customer)
        db_contract = create_new_contract(db_customer)
        assert db_contract.customer_assigned == db_customer
        assert db_contract.id == "CT00001"
        print(db_contract)

    def test_03_create_new_event(self):
        """create new event for a contract
        """
        user_sales = create_new_user_sales()
        print(user_sales)
        user_support = create_new_user_support()
        print(user_support)
        db_customer = create_new_customer(user_sales)
        print(db_customer)
        db_contract = create_new_contract(db_customer)
        print(db_contract)
        db_event = create_new_event(db_contract, user_support)
        print(db_event)

    def test_04_create_new_need(self):
        """create new need for a event
        """
        user_sales = create_new_user_sales()
        print(user_sales)
        user_support = create_new_user_support()
        print(user_support)
        db_customer = create_new_customer(user_sales)
        print(db_customer)
        db_contract = create_new_contract(db_customer)
        print(db_contract)
        db_event = create_new_event(db_contract, user_support)
        print(db_event)
        db_need = create_new_need(db_event)
        print(db_need)
