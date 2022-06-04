from django.test import Client, TestCase
from django.urls import reverse
from authentication.models import ProfileStaff, User

from crm.models import Customer

# Test_Number_verbHTML_codeHTML__reversename


class TestUnitaireApiCustomer(TestCase):
    @classmethod
    def setup_class(cls):
        profile_staff = ProfileStaff.objects.filter(
            name="SALES").first()
        user_sales = User.objects.filter(
            profile_staff=profile_staff).first()
        new_customer = Customer.objects.create(
            first_name="Brian",
            last_name="Werndow",
            email="brian.w@musicevents.com",
            phone="0123456789",
            mobile="0601020301",
            company_name="Music Events",
            sales_contact=user_sales
        )
        new_customer.save()

    def test_01_get_all__customers(self):
        print(Customer.objects.all())
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("customers"))
        assert response.status_code == 202
        print(response.data)
        assert (response.data[0].get("id", "")) == "CM00001"
        assert (response.data[0].get("first_name", "")) == "Tony"
        assert (response.data[0].get("last_name", "")) == "Bornes"
        assert (response.data[0].get(
            "email", "")) == "tonybornes@entreprise.com"

    def test_01_get_all_401__customers(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'no_access@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("customers"))
        assert response.status_code == 401

    def test_02_post_202__customers(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.post(
            reverse("customers"),
            data={
                "first_name": "Brian",
                "last_name": "Werndow",
                "email": "brian.w2@musicevents.com",
                "phone": "0123456789",
                "mobile": "0601020301",
                "company_name": "Music Events",
                "sales_contact__email": "sales2@epicevents.fr"
            })
        print(response)
        assert response.status_code == 202
    
    def test_02_post_401_profile__customers(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'no_access@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.post(
            reverse("customers"),
            data={
                "first_name": "Brian",
                "last_name": "Werndow",
                "email": "brian.w2@musicevents.com",
                "phone": "0123456789",
                "mobile": "0601020301",
                "company_name": "Music Events",
                "sales_contact__email": "sales2@epicevents.fr"
            })
        print(response)
        assert response.status_code == 401

    def test_02_post_406_email_already_used__customers(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.post(
            reverse("customers"),
            data={
                "first_name": "Brian2",
                "last_name": "Werndow2",
                "email": "brian.w@musicevents.com",
                "phone": "01234567892",
                "mobile": "06010203012",
                "company_name": "Music Events2",
                "sales_contact__email": "sales2@epicevents.fr"
            })
        print(response)
        assert response.status_code == 406

    def test_02_post_401__customers(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'support@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.post(
            reverse("customers"),
            data={
                "first_name": "Brian",
                "last_name": "Werndow",
                "email": "brian.w@musicevents.com",
                "phone": "0123456789",
                "company_name": "Music Events",
                "sales_contact__email": "sales2@epicevents.fr"
            })
        assert response.status_code == 401
        print(response.data)

    def test_02_post_406_error_email_sales__customers(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'sales@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.post(
            reverse("customers"),
            data={
                "first_name": "Brian",
                "last_name": "Werndow",
                "email": "brian.w3@musicevents.com",
                "phone": "0123456789",
                "company_name": "Music Events",
                "sales_contact__email": "sales55@epicevents.fr"
            })
        assert response.status_code == 406
        print(response.data)

    def test_02_post_406_other__customers(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'sales@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.post(
            reverse("customers"),
            data={
                "first_name": "Brian",
                "email": "brian.w6@musicevents.com",
                "phone": "0123456789",
                "company_name": "Music Events",
                "sales_contact__email": "sales@epicevents.fr"
            })
        assert response.status_code == 406
        print(response.data)

    def test_02_post_401__customers(self):
        client = Client()
        response = client.post(
            reverse("customers"),
            data={
                "first_name": "Brian",
                "last_name": "Werndow",
                "email": "brian.w@musicevents.com",
                "phone": "0123456789",
                "company_name": "Music Events",
                "sales_contact__email": "sales1@epicevents.fr"
            })
        assert response.status_code == 401
        print(response.data)

    def test_03_get_202__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        id_custo = Customer.objects.all().last().id
        print(id_custo)
        print(Customer.objects.all())
        response = client.get(
            reverse("customer", kwargs={'id_customer': id_custo}))
        print(response.data)
        assert response.status_code == 202

    def test_03_get_401__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'no_access@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        id_custo = Customer.objects.all().last().id
        response = client.get(
            reverse("customer", kwargs={'id_customer': id_custo}))
        print(response.data)
        assert response.status_code == 401

    def test_04_put_202_manage__customer(self):
        print(Customer.objects.all())
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.put(
            reverse("customer", kwargs={'id_customer': "CM00002"}),
            data={
                "first_name": "Brian2",
                "last_name": "Werndow2",
                "email": "brian.w2@musicevents.com",
                "phone": "01234567892",
                "mobile": "06010203012",
                "company_name": "Music Events2",
                "sales_contact__email": "sales@epicevents.fr"
            },
            content_type='application/json')
        print(response.data)
        assert response.status_code == 202

    def test_04_put_406_manage_error_Salescontact__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.put(
            reverse("customer", kwargs={'id_customer': "CM00001"}),
            data={
                "first_name": "Brian2",
                "last_name": "Werndow2",
                "email": "brian.w2@musicevents.com",
                "phone": "01234567892",
                "mobile": "06010203012",
                "company_name": "Music Events2",
                "sales_contact__email": "sales44@epicevents.fr"
            },
            content_type='application/json')
        print(response.data)
        assert response.status_code == 406

    def test_04_put_202_sales__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'sales@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.put(
            reverse("customer", kwargs={'id_customer': "CM00001"}),
            data={
                "first_name": "Brian3",
                "last_name": "Werndow3",
                "email": "brian.w2@musicevents.com",
                "phone": "01234567892",
                "mobile": "06010203012",
                "company_name": "Music Events3",
                "sales_contact__email": "sales@epicevents.fr"
            },
            content_type='application/json')
        print(response.data)
        assert response.status_code == 202

    def test_04_put_406_sales__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'sales@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.put(
            reverse("customer", kwargs={'id_customer': "CM00001"}),
            data={
                "first_name": "Brian3",
                "last_name": "Werndow3",
                "email": "brian.w2@musicevents.com",
                "phone": "01234567892",
                "mobile": "06010203012",
                "company_name": "Music Events3",
                "sales_contact__email": "sales55@epicevents.fr"
            },
            content_type='application/json')
        print(response.data)
        assert response.status_code == 406

    def test_04_put_401__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'no_access@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.put(
            reverse("customer", kwargs={'id_customer': "CM00001"}),
            data={
                "first_name": "Brian2",
                "last_name": "Werndow2",
                "email": "brian.w2@musicevents.com",
                "phone": "01234567892",
                "mobile": "06010203012",
                "company_name": "Music Events2",
                "sales_contact__email": "sales@epicevents.fr"
            })
        print(response.data)
        assert response.status_code == 401

    def test_04_put_406__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.put(
            reverse("customer", kwargs={'id_customer': "CM00001"}),
            data={
                "first_name": "Brian2",
                "last_name": "Werndow2",
                "phone": "01234567892",
                "mobile": "06010203012",
                "company_name": "Music Events2",
                "sales_contact__email": "sales@epicevents.fr"
            },
            content_type='application/json')
        assert response.status_code == 406

    def test_05_delete_202__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.delete(
            reverse("customer", kwargs={'id_customer': "CM00001"}))
        print(response.data)
        assert response.status_code == 202

    def test_05_delete_401__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'no_access@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.delete(
            reverse("customer", kwargs={'id_customer': "CM00001"}))
        print(response.data)
        assert response.status_code == 401

    def test_06__search_by_mail_401__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'no_access@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("customer_search_mail",
                    kwargs={'mail': "brian.w@musicevents.com"}))
        print(response.data)
        assert response.status_code == 401

    def test_06__search_by_mail_202__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("customer_search_mail",
                    kwargs={'mail': "brian.w@musicevents.com"}))
        print(response.data)
        assert response.status_code == 202

    def test_06__search_by_mail_204__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("customer_search_mail",
                    kwargs={'mail': "brian.w3@musicevents.com"}))
        print(response.data)
        assert response.status_code == 204

    def test_06__search_by_mail_406format__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("customer_search_mail",
                    kwargs={'mail': "brian.w3@musicevents"}))
        print(response.data)
        assert response.status_code == 406

    def test_07__search_by_sales_contact_202__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("customer_search_sales",
                    kwargs={'mail': "sales@epicevents.fr"}))
        print(response.data)
        assert response.status_code == 202

    def test_07__search_by_sales_contact_401__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'no_access@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("customer_search_sales",
                    kwargs={'mail': "sales@epicevents.fr"}))
        print(response.data)
        assert response.status_code == 401

    def test_07__search_by_sales_contact_406_mail_format__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'sales@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("customer_search_sales",
                    kwargs={'mail': "sales@epicevents"}))
        print(response.data)
        assert response.status_code == 406

    def test_07__search_by_sales_contact_400_nomaildb__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'sales@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("customer_search_sales",
                    kwargs={'mail': "sales@epicevents.sr"}))
        print(response.data)
        assert response.status_code == 400

    def test_07__search_by_sales_contact_400_mail_support__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("customer_search_sales",
                    kwargs={'mail': "support@epicevents.fr"}))
        print(response.data)
        assert response.status_code == 400

    def test_07__search_by_sales_contact_204_no_customer__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("customer_search_sales",
                    kwargs={'mail': "sales2@epicevents.fr"}))
        print(response.data)
        assert response.status_code == 204

    def test_08__search_by_name_202_lf__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get('%s?first_name=%s&last_name=%s' % (
            reverse("customer_search_name"), "Brian", "Werndow"))
        print(response.data)
        assert response.status_code == 202

    def test_08__search_by_name_202_l__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get('%s?last_name=%s' % (
            reverse("customer_search_name"), "Werndow"))
        print(response.data)
        assert response.status_code == 202

    def test_08__search_by_name_202_f__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get('%s?first_name=%s' % (
            reverse("customer_search_name"), "Brian"))
        print(response.data)
        assert response.status_code == 202

    def test_08__search_by_name_406_f__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get('%s?first_name=%s' % (
            reverse("customer_search_name"), "Brian3"))
        print(response.data)
        assert response.status_code == 406

    def test_08__search_by_name_406_noneinput__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(reverse("customer_search_name"))
        print(response.data)
        assert response.status_code == 406

    def test_08__search_by_name_401__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'no_access@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(reverse("customer_search_name"))
        print(response.data)
        assert response.status_code == 401