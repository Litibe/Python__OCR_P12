from django.test import Client, TestCase
from django.urls import reverse

from crm import models

# Test_Number_verbHTML_codeHTML__reversename


class TestUnitaireApiCustomer(TestCase):
    def test_01_get_all__customers(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("customers"))
        assert response.status_code == 202
        assert (response.data[0].get("id", "")) == "CM00001"
        assert (response.data[0].get("first_name", "")) == "Tony"
        assert (response.data[0].get("last_name", "")) == "DURAND"
        assert (response.data[0].get(
            "email", "")) == "tonydurant@entreprise.com"
        sales_customer1 = models.Customer.objects.all().first()
        sales_customer1 = sales_customer1.sales_contact.email
        response_api_sales = response.data[0].get(
            "sales_contact", "")
        assert (response_api_sales.get("email", "")) == sales_customer1
        assert (response.data[1].get("id", "")) == "CM00002"

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
                "email": "brian.w@musicevents.com",
                "phone": "0123456789",
                "mobile": "0601020301",
                "company_name": "Music Events",
                "sales_contact__email": "sales2@epicevents.fr"
            })
        print(response.data)
        assert response.status_code == 202

    def test_02_post_401__customers(self):
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
                "email": "brian.w@musicevents.com",
                "phone": "0123456789",
                "mobile": "0601020301",
                "company_name": "Music Events",
                "sales_contact__email": "sales2@epicevents.fr"
            })
        print(response.data)
        assert response.status_code == 401

    def test_03_post_401__customers(self):
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

    def test_03_post_406_error_email_sales__customers(self):
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
                "email": "brian.w@musicevents.com",
                "phone": "0123456789",
                "company_name": "Music Events",
                "sales_contact__email": "sales55@epicevents.fr"
            })
        assert response.status_code == 406
        print(response.data)

    def test_04_post_401__customers(self):
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

    def test_05_get_202__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        id_custo = models.Customer.objects.all().last().id
        print(id_custo)
        response = client.get(
            reverse("customer", kwargs={'id_customer': id_custo}))
        print(response.data)
        assert response.status_code == 202

    def test_05_get_401__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'no_access@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        id_custo = models.Customer.objects.all().last().id
        response = client.get(
            reverse("customer", kwargs={'id_customer': id_custo}))
        print(response.data)
        assert response.status_code == 401

    def test_06_put_202_manage__customer(self):
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

    def test_06_put_406_manage_error_Salescontact__customer(self):
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
                "sales_contact__email": "sales44@epicevents.fr"
            },
            content_type='application/json')
        print(response.data)
        assert response.status_code == 406

    def test_06_put_202_sales__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'sales2@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.put(
            reverse("customer", kwargs={'id_customer': "CM00002"}),
            data={
                "first_name": "Brian3",
                "last_name": "Werndow3",
                "email": "brian.w2@musicevents.com",
                "phone": "01234567892",
                "mobile": "06010203012",
                "company_name": "Music Events3",
                "sales_contact__email": "sales2@epicevents.fr"
            },
            content_type='application/json')
        print(response.data)
        assert response.status_code == 202

    def test_06_put_406_sales__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'sales2@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.put(
            reverse("customer", kwargs={'id_customer': "CM00002"}),
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
        assert response.status_code == 406

    def test_07_put_401__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'no_access@epicevents.fr',
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
            })
        print(response.data)
        assert response.status_code == 401

    def test_08_put_406__customer(self):
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
                "phone": "01234567892",
                "mobile": "06010203012",
                "company_name": "Music Events2",
                "sales_contact__email": "sales@epicevents.fr"
            },
            content_type='application/json')
        print(response.data)
        assert response.status_code == 406

    def test_09_delete_202__customer(self):
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

    def test_10_write_delete_401__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'no_access@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.delete(
            reverse("customer", kwargs={'id_customer': "CM00002"}))
        print(response.data)
        assert response.status_code == 401


class TestUnitaireApiContract(TestCase):
    def test_00_get_all__contracts(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("contracts"))
        assert response.status_code == 202
        assert (response.data[0].get("id", "")) == "CT00001"
        print(response.data)

    def test_01_get_all_401__contracts(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'no_access@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("contracts"))
        assert response.status_code == 401
        print(response.data)

    def test_02_get_404__contract(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("contract", kwargs={'id_contract': "CT000001"}),
            content_type='application/json')
        assert response.status_code == 404

    def test_03_get_202__contract(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("contract", kwargs={'id_contract': "CT00001"}),
            content_type='application/json')
        assert response.status_code == 202
        assert (response.data.get("id", "")) == "CT00001"
        print(response.data)

    def test_04_get_401__contract(self):
        client = Client()
        response = client.get(
            reverse("contract", kwargs={'id_contract': "CT00001"}),
            content_type='application/json')
        assert response.status_code == 401

    def test_05_get_202__contract(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("contract", kwargs={'id_contract': "CT00001"}),
            content_type='application/json')
        assert response.status_code == 202
        assert (response.data.get("id", "")) == "CT00001"

    def test_06_post_202__contracts(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.post(
            reverse("contracts"),
            data={
                "title": "Contract Conges Beach Summer 22",
                "date_start_contract": "2022-06-03 08:00",
                "date_end_contract": "2022-07-16 19:00",
                "signed": "True",
                "customer_assigned__id": "CM00002"
                },
            content_type='application/json')
        print(response.data)
        assert response.status_code == 202

    def test_06_post_400__contracts(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'sales@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.post(
            reverse("contracts"),
            data={
                "title": "Contract Conges Beach Summer 22",
                "date_start_contract": "2022-06-03 08:00",
                "date_end_contract": "2022-07-16 19:00",
                "signed": "True",
                "customer_assigned__id": "CM00202"
                },
            content_type='application/json')
        print(response.data)
        assert response.status_code == 400

    def test_07_post_401_support_unautho__contracts(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'support@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.post(
            reverse("contracts"),
            data={
                "title": "Contract Conges Beach Summer 23",
                "date_start_contract": "2023-06-03 08:00",
                "date_end_contract": "2023-07-16 19:00",
                "signed": "True",
                "customer_assigned__id": "CM00002"
                },
            content_type='application/json')
        print(response.data)
        assert response.status_code == 401

    def test_08_put_401_sales_update__contract(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'sales@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.put(
            reverse("contract", kwargs={'id_contract': "CT00002"}),
            data={
                "title": "Contract Conges Beach Summer 44",
                "date_start_contract": "2022-06-03 08:00",
                "date_end_contract": "2022-07-16 19:00",
                "signed": "False",
                "customer_assigned__id": "CM00002"
                },
            content_type='application/json')
        print(response.data)
        assert response.status_code == 401

    def test_09_put_406_customer_error__contract(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.put(
            reverse("contract", kwargs={'id_contract': "CT00002"}),
            data={
                "title": "Contract Conges Beach Summer 44",
                "date_start_contract": "2022-06-03 08:00",
                "date_end_contract": "2022-07-16 19:00",
                "signed": "False",
                "customer_assigned__id": "CM20002"
                },
            content_type='application/json')
        print(response.data)
        assert response.status_code == 406

    def test_09_put_401_saleserror__contract(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'sales@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.put(
            reverse("contract", kwargs={'id_contract': "CT00002"}),
            data={
                "title": "Contract Conges Beach Summer 44",
                "date_start_contract": "2022-06-03 08:00",
                "date_end_contract": "2022-07-16 19:00",
                "signed": "False",
                "customer_assigned__id": "CM00002"
                },
            content_type='application/json')
        print(response.data)
        assert response.status_code == 401

    def test_09_put_202_sales_update__contract(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'sales2@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.put(
            reverse("contract", kwargs={'id_contract': "CT00002"}),
            data={
                "title": "Contract Conges Beach Summer 44",
                "date_start_contract": "2022-06-03 08:00",
                "date_end_contract": "2022-07-16 19:00",
                "signed": "False",
                "customer_assigned__id": "CM00002"
                },
            content_type='application/json')
        print(response.data)
        assert response.status_code == 202

    def test_10_del_401___contract(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'sales2@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.delete(
            reverse("contract", kwargs={'id_contract': "CT00002"}))
        print(response.data)
        assert response.status_code == 401

    def test_10_del_404___contract(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'sales2@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.delete(
            reverse("contract", kwargs={'id_contract': "CT00202"}))
        print(response.data)
        assert response.status_code == 404

    def test_10_del_202___contract(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.delete(
            reverse("contract", kwargs={'id_contract': "CT00002"}))
        print(response.data)
        assert response.status_code == 202


class TestUnitaireApiEvent(TestCase):
    def test_00_get_all__events(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("events"))
        assert response.status_code == 202
        assert (response.data[0].get("id", "")) == "E00001"
        print(response.data)

    def test_01_get_all_401__events(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'no_access@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("events"))
        assert response.status_code == 401
        print(response.data)

    def test_02_get_202___event(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("event", kwargs={'id_event': "E00001"}))
        print(response.data)
        assert response.status_code == 202

    def test_03_post_401__events(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'no_access@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.post(
            reverse("events"),
            data={
                "title": "Contract Conges Beach Summer 22",
                "date_started": "2022-06-03 08:00",
                "date_finished": "2022-07-16 19:00",
                "signed": "True",
                "support_contact__email": "support@epicevents.com",
                "contract_assigned__id": "CT00001"
                },
            content_type='application/json')
        print(response.data)
        assert response.status_code == 401

    def test_03_post_202__events(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'sales@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.post(
            reverse("events"),
            data={
                "title": "Contract Conges Beach Summer 22",
                "date_started": "2022-06-03 08:00",
                "date_finished": "2022-07-16 19:00",
                "signed": "True",
                "support_contact__email": "support@epicevents.fr",
                "contract_assigned__id": "CT00002"
                },
            content_type='application/json')
        print(response.data)
        assert response.status_code == 202

    def test_03_post_400_support__events(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'sales@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.post(
            reverse("events"),
            data={
                "title": "Contract Conges Beach Summer 22",
                "date_started": "2022-06-03 08:00",
                "date_finished": "2022-07-16 19:00",
                "signed": "True",
                "support_contact__email": "support22@epicevents.com",
                "contract_assigned__id": "CT00001"
                },
            content_type='application/json')
        print(response.data)
        assert response.data == (
            "Error Support_contact email assigned not existing")
        assert response.status_code == 400

    def test_03_post_400_contract__events(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'sales@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.post(
            reverse("events"),
            data={
                "title": "Contract Conges Beach Summer 22",
                "date_started": "2022-06-03 08:00",
                "date_finished": "2022-07-16",
                "signed": "True",
                "support_contact__email": "support@epicevents.fr",
                "contract_assigned__id": "CT20001"
                },
            content_type='application/json')
        assert response.status_code == 400

    def test_04_get_401___event(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'no_access@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("event", kwargs={'id_event': "E00001"}))
        print(response.data)
        assert response.status_code == 401

    def test_04_get_202___event(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'support@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("event", kwargs={'id_event': "E00001"}))
        print(response.data)
        assert response.status_code == 202

    def test_05_put_202_contract__events(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'support@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.put(
            reverse("event", kwargs={'id_event': "E00001"}),
            data={
                "title": "Contract Conges Beach Summer 22",
                "date_started": "2022-06-03 08:00",
                "date_finished": "2022-07-18 08:00",
                "signed": "True",
                "support_contact__email": "support@epicevents.fr",
                "contract_assigned__id": "CT00001"
                },
            content_type='application/json')
        assert response.status_code == 202

    def test_05_put_400_contract__events(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'support@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.put(
            reverse("event", kwargs={'id_event': "E00001"}),
            data={
                "title": "Contract Conges Beach Summer 22",
                "date_started": "2022-06-03 08:00",
                "date_finished": "2022-07-18 08:00",
                "signed": "True",
                "support_contact__email": "support@epicevents.fr",
                "contract_assigned__id": "CT01001"
                },
            content_type='application/json')
        assert response.status_code == 400
        assert response.data == "Error ID Contract assigned"

    def test_05_put_400_supportuser__events(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'support@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.put(
            reverse("event", kwargs={'id_event': "E00001"}),
            data={
                "title": "Contract Conges Beach Summer 22",
                "date_started": "2022-06-03 08:00",
                "date_finished": "2022-07-18 08:00",
                "signed": "True",
                "support_contact__email": "support33@epicevents.fr",
                "contract_assigned__id": "CT00001"
                },
            content_type='application/json')
        print(response.data)
        assert response.status_code == 400
        assert response.data == (
            "Error Support_contact email assigned not existing")

    def test_05_put_400_supportuserprofile__events(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'support@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.put(
            reverse("event", kwargs={'id_event': "E00001"}),
            data={
                "title": "Contract Conges Beach Summer 22",
                "date_started": "2022-06-03 08:00",
                "date_finished": "2022-07-18 08:00",
                "signed": "True",
                "support_contact__email": "sales@epicevents.fr",
                "contract_assigned__id": "CT00001"
                },
            content_type='application/json')
        print(response.data)
        assert response.status_code == 400
        assert response.data == (
            "Error Support_contact email assigned not profile SUPPORT")

    def test_05_put_401_contract__events(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'sales2@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.put(
            reverse("event", kwargs={'id_event': "E00001"}),
            data={
                "title": "Contract Conges Beach Summer 22",
                "date_started": "2022-06-03 08:00",
                "date_finished": "2022-07-18 08:00",
                "signed": "True",
                "support_contact__email": "support@epicevents.fr",
                "contract_assigned__id": "CT00001"
                },
            content_type='application/json')
        assert response.status_code == 401

    def test_06_del_401___event(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'support@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.delete(
            reverse("event", kwargs={'id_event': "E00001"}))
        print(response.data)
        assert response.status_code == 401

    def test_06_del_202___event(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.delete(
            reverse("event", kwargs={'id_event': "E00001"}))
        print(response.data)
        assert response.status_code == 202


class TestUnitaireApiNeed(TestCase):
    def test_00_get_all__needs(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("needs"))
        assert response.status_code == 202
        assert (response.data[0].get("id", "")) == "N00001"
        print(response.data)

    def test_01_get_all_401__needs(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'no_access@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("needs"))
        assert response.status_code == 401
        print(response.data)

    def test_02_get_202___need(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'support@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("need", kwargs={'id_need': "N00001"}))
        print(response.data)
        assert response.status_code == 202

    def test_02_get_401___need(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'no_access@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("need", kwargs={'id_need': "N00001"}))
        print(response.data)
        assert response.status_code == 401

    def test_03_post_202__needs(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'support@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.post(
            reverse("needs"),
            data={
                "title": "Office with Computer and internet",
                "success": "True",
                "event_assigned__id": "E00001"
                },
            content_type='application/json')
        print(response.data)
        assert response.status_code == 202

    def test_04_put_202__need(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'support@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.put(
            reverse("need", kwargs={'id_need': "N00001"}),
            data={
                "title": "Office with Computer and internet",
                "success": "False",
                "event_assigned__id": "E00001"
                },
            content_type='application/json')
        assert response.status_code == 202

    def test_04_put_401__need(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'sales2@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.put(
            reverse("need", kwargs={'id_need': "N00001"}),
            data={
                "title": "Office with Computer and internet",
                "success": "False",
                "event_assigned__id": "E00001"
                },
            content_type='application/json')
        assert response.status_code == 401

    def test_04_put_400__need(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'support@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.put(
            reverse("need", kwargs={'id_need': "N00001"}),
            data={
                "title": "Office with Computer and internet",
                "success": "True",
                "event_assigned__id": "E00202"
                },
            content_type='application/json')
        assert response.status_code == 400

    def test_05_delete_401__need(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'sales@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.delete(
            reverse("need", kwargs={'id_need': "N00001"}))
        assert response.status_code == 401

    def test_05_delete_202__need(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.delete(
            reverse("need", kwargs={'id_need': "N00001"}))
        assert response.status_code == 202
