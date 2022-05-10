from django.test import Client, TestCase
from django.urls import reverse

from crm import models


class TestUnitaireApiCustomer(TestCase):
    def test_01_get_all__read_customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("read_customer"))
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

    def test_02_post_202__read_customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.post(
            reverse("read_customer"),
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

    def test_03_post_406__read_customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.post(
            reverse("read_customer"),
            data={
                "first_name": "Brian",
                "last_name": "Werndow",
                "email": "brian.w@musicevents.com",
                "phone": "0123456789",
                "company_name": "Music Events",
                "sales_contact__email": "sales2@epicevents.fr"
            })
        assert response.status_code == 406
        print(response.data)

    def test_04_post_401__read_customer(self):
        client = Client()
        response = client.post(
            reverse("read_customer"),
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

    def test_06_put_202__customer(self):
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

    def test_07_put_401__customer(self):
        client = Client()
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

    def test_10_write_delete_404__customer(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.delete(
            reverse("customer", kwargs={'id_customer': "CM00002"}))
        print(response.data)
        assert response.status_code == 202


class TestUnitaireApiContract(TestCase):
    def test_00_get_all__read_contract(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("read_contract"))
        assert response.status_code == 202
        assert (response.data[0].get("id", "")) == "CT00001"
        print(response.data)

    def test_01_get_all_401__read_contract(self):
        client = Client()
        response = client.get(
            reverse("read_contract"))
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
        print(response.data)

    def test_06_post_202__read_contract(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("read_contract"),
            data={
                "title": "Contract Conges Beach Summer 22",
                "date_start_contract": "2022-06-03 08:00",
                "date_end_contract": "2022-07-16 19:00",
                "signed": "True",
                "customer_assigned__id": "CM00002"
                },
            content_type='application/json')
        assert response.status_code == 202
        print(response.data)

    def test_06_post_401_support_unautho__read_contract(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'support@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.post(
            reverse("read_contract"),
            data={
                "title": "Contract Conges Beach Summer 22",
                "date_start_contract": "2022-06-03 08:00",
                "date_end_contract": "2022-07-16 19:00",
                "signed": "True",
                "customer_assigned__id": "CM00002"
                },
            content_type='application/json')
        assert response.status_code == 401

    def test_06_put_202_sales_update__read_contract(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'sales@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.put(
            reverse("read_contract"),
            data={
                "title": "Contract Conges Beach Summer 44",
                "date_start_contract": "2022-06-03 08:00",
                "date_end_contract": "2022-07-16 19:00",
                "signed": "False",
                "customer_assigned__id": "CM00002"
                },
            content_type='application/json')
        assert response.status_code == 202
