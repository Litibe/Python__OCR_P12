from django.test import Client, TestCase
from django.urls import reverse

from crm.models import Customer, Contract


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
                "amount": 2000,
                "customer_assigned__id": "CM00002"
                },
            content_type='application/json')
        print(response.data)
        assert response.status_code == 202

    def test_06_post_401_sales_contact__contracts(self):
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
                "amount": "6000",
                "customer_assigned__id": "CM00002"
                },
            content_type='application/json')
        print(response.data)
        assert response.status_code == 202

    def test_06_post_406__contracts(self):
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
                "date_end_contract": "2022-07-16 19:00",
                "customer_assigned__id": "CM00002"
                },
            content_type='application/json')
        print(response.data)
        assert response.status_code == 406

    def test_06_post_400_customer__contracts(self):
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
                "amount": "6000",
                "customer_assigned__id": "CM00009"
                },
            content_type='application/json')
        print(response.data)
        assert response.status_code == 400

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
                "amount": "6000",
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
                "amount": "6000",
                "customer_assigned__id": "CM00002"
                },
            content_type='application/json')
        print(response.data)
        assert response.status_code == 401

    def test_08_put_401_sales_update__contract(self):
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
                "amount": "6000",
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
                "amount": "6000",
                "customer_assigned__id": "CM20002"
                },
            content_type='application/json')
        print(response.data)
        assert response.status_code == 406

    def test_09_put_202_sales_update__contract(self):
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
                "amount": "6000",
                "customer_assigned__id": "CM00002"
                },
            content_type='application/json')
        print(response.data)
        assert response.status_code == 202

    def test_09_put_406_no_date__contract(self):
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
                "signed": "False",
                "amount": "6000",
                "customer_assigned__id": "CM00002"
                },
            content_type='application/json')
        print(response.data)
        assert response.status_code == 406

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

    def test_11_delete_404___contract(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'no_access@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.delete(
            reverse("contract", kwargs={'id_contract': "CT00002"}))
        print(response.data)
        assert response.status_code == 401

    def test_11_get_404___contract(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'no_access@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("contract", kwargs={'id_contract': "CT00002"}))
        print(response.data)
        assert response.status_code == 401
