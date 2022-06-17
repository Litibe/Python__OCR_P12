from django.test import Client, TestCase
from django.urls import reverse


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
                "support_contact__email": "support@epicevents.fr",
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
                "support_contact__email": "support@epicevents.fr",
                "contract_assigned__id": "CT00001"
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
                "support_contact__email": "support22@epicevents.com",
                "contract_assigned__id": "CT00001"
                },
            content_type='application/json')
        print(response.data)
        assert response.data == (
            "Error Support_contact email assigned not existing")
        assert response.status_code == 400

    def test_03_post_400_contract_not_signed__events(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'sales@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.post(
            reverse("events"),
            data={
                "title": "Conges Beach Summer 22",
                "date_started": "2022-06-03 08:00",
                "date_finished": "2022-07-16 19:00",
                "support_contact__email": "support@epicevents.com",
                "contract_assigned__id": "CT00002"
                },
            content_type='application/json')
        print(response.data)
        assert response.data == ("Error Contract not signed !")
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
                "support_contact__email": "support@epicevents.fr",
                "contract_assigned__id": "CT20001"
                },
            content_type='application/json')
        assert response.status_code == 400

    def test_03_post_400_not_contractId__events(self):
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
                "support_contact__email": "sales2@epicevents.fr",
                "contract_assigned__id": "CT20001"
                },
            content_type='application/json')
        assert response.status_code == 400

    def test_03_post_400_not_support__events(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.post(
            reverse("events"),
            data={
                "title": "Contract Conges Beach Summer 22",
                "date_started": "2022-06-03 08:00",
                "date_finished": "2022-07-16",
                "support_contact__email": "sales@epicevents.fr",
                "contract_assigned__id": "CT00001"
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

    def test_07__search_by_date_start_401__event(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'no_access@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("event_by_date_start",
                    kwargs={'date': "2022-06-03"}))
        print(response.data)
        assert response.status_code == 401

    def test_07__search_by_date_start_202__event(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("event_by_date_start",
                    kwargs={'date': "2022-08-03"}))
        print(response.data)
        assert response.status_code == 202

    def test_07__search_by_date_start_204__event(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("event_by_date_start",
                    kwargs={'date': "2023-06-03"}))
        print(response.data)
        assert response.status_code == 204

    def test_07__search_by_date_end_401__event(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'no_access@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("event_by_date_end",
                    kwargs={'date': "2022-06-03"}))
        print(response.data)
        assert response.status_code == 401

    def test_07__search_by_date_end_202__event(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("event_by_date_end",
                    kwargs={'date': "2022-08-03"}))
        print(response.data)
        assert response.status_code == 202

    def test_07__search_by_date_end_204__event(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("event_by_date_end",
                    kwargs={'date': "2023-06-03"}))
        print(response.data)
        assert response.status_code == 204

    def test_08__search_by_name_customer_202_l__event(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'sales@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get('%s?last_name=%s' % (
            reverse("event_by_name_customer"), "Bornes"))
        print(response.data)
        assert response.status_code == 202

    def test_08__search_by_name_customer_202_f__event(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'sales@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get('%s?first_name=%s' % (
            reverse("event_by_name_customer"), "Tony"))
        print(response.data)
        assert response.status_code == 202

    def test_08__search_by_name_customer_204_lf__event(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'sales@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get('%s?first_name=%s&last_name=%s' % (
            reverse("event_by_name_customer"), "Brian", "Werndow"))
        print(response.data)
        assert response.status_code == 204

    def test_08__search_by_name_customer_202_lf__contract(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'sales@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get('%s?first_name=%s&last_name=%s' % (
            reverse("event_by_name_customer"), "Tony", "Bornes"))
        print(response.data)
        assert response.status_code == 202

    def test_08__search_by_name_customer_406_lf__event(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'sales@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get('%s?first_name=%s&last_name=%s' % (
            reverse("event_by_name_customer"), "Brin", "Wernd"))
        print(response.data)
        assert response.status_code == 406

    def test_08__search_by_name_customer_401__evnet(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'no_access@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get('%s?last_name=%s' % (
            reverse("event_by_name_customer"), "Werndow"))
        print(response.data)
        assert response.status_code == 401

    def test_08__search_by_name_customer_406__event(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'sales@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(reverse("event_by_name_customer"))
        print(response.data)
        assert response.data == (
            "Please verify last_name and/or first_name  input!")
        assert response.status_code == 406

    def test_09__search_by_mail_customer_202__event(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("event_by_email_customer",
                    kwargs={'mail': "tonybornes@entreprise.com"}))
        print(response.data)
        assert response.status_code == 202

    def test_09__search_by_mail_customer_401__event(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'no_access@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("event_by_email_customer",
                    kwargs={'mail': "tonybornes@entreprise.com"}))
        print(response.data)
        assert response.status_code == 401

    def test_09__search_by_mail_customer_204__event(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'manage@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("event_by_email_customer",
                    kwargs={'mail': "tony@entreprise.fr"}))
        print(response.data)
        assert response.status_code == 204

    def test_09__search_by_mail_customer_204_no_contract__event(self):
        client = Client()
        response = client.post(reverse("login"),
                               data={'email': 'support@epicevents.fr',
                                     'password': 'epicevents'})
        access_token = 'Bearer ' + response.data.get('access')
        client.defaults['HTTP_AUTHORIZATION'] = access_token
        response = client.get(
            reverse("event_by_email_customer",
                    kwargs={'mail': "brian.w@musicevents.com"}))
        print(response.data)
        assert response.status_code == 204
