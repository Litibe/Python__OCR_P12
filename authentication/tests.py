from urllib import response
import pytest
from django.test import Client
from django.urls import reverse, resolve


@pytest.mark.django_db
def test_create_new_user_error():
    client = Client()
    response = client.post(reverse("sign_up"), data={'key1': 'data1',
                                                     'key2': 'data2'})
    assert response.status_code == 406


@pytest.mark.django_db
def test_create_new_user_success():
    client = Client()
    response = client.post(reverse("sign_up"),
                           data={'email': 'lioneltissier2@epicevents.fr',
                                 'first_name': 'Lionel2',
                                 'last_name': 'TISSIER2',
                                 'password': 'epicevents',
                                 'profile': "MANAGE"})
    assert response.status_code == 201
