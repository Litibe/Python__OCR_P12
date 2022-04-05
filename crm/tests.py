import datetime
from django.test import TestCase
from authentication.models import ProfileStaff, User

from crm.models import Contract, Customer


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


class TestUnitaireModels(TestCase):
    """ Class TEST Unitaire for Models CRM """
    def test_01_create_new_customer(self):
        """create new user_sales into db and new customer with sales_contact
        """
        self.user_sales = create_new_user_sales()
        self.db_customer = create_new_customer(self.user_sales)
        assert self.db_customer.id == 1
        assert self.db_customer.first_name == "Tony"
        assert self.db_customer.sales_contact.profile_staff.name == "SALES"

    def test_02_create_new_contract(self):
        """create new contract for a customer
        """
        self.user_sales = create_new_user_sales()
        self.db_customer = create_new_customer(self.user_sales)
        assert self.db_customer.id == 2
        self.db_contract = create_new_contract(self.db_customer)
        assert self.db_contract.customer_assigned == self.db_customer
        assert self.db_contract.id == "CT00001"
