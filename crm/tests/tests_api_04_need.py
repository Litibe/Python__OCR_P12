from django.test import Client, TestCase
from django.urls import reverse


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

    def test_03_post_400_id__needs(self):
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
                "event_assigned__id": "E20001"
                },
            content_type='application/json')
        print(response.data)
        assert response.status_code == 400

    def test_03_post_400__needs(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'support@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.post(
            reverse("needs"),
            data={
                "success": "True",
                "event_assigned__id": "E20001"
                },
            content_type='application/json')
        print(response.data)
        assert response.status_code == 400

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
