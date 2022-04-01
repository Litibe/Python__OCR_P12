from django.test import TestCase
from authentication.models import ProfileStaff, User

from crm.models import Contract, Customer


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


def create_new_user_sales():
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
    new_contract = Contract.objects.create(
        
    )

class TestUnitaireModels(TestCase):
    def test_create_new_customer(self):
        user_sales = create_new_user_sales()
        db_customer = create_new_customer(user_sales)
        assert db_customer.id == 1
        assert db_customer.first_name == "Tony"
        assert db_customer.sales_contact.profile_staff.name == "SALES"

    def test_create_new_contract(self):
        user_sales = create_new_user_sales()
        db_customer = create_new_customer(user_sales)
        assert db_customer.id == 1


