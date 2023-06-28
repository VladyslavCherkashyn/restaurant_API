import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from mixer.backend.django import mixer
from user.serializers import UserSerializer


User = get_user_model()


@pytest.fixture
def user():
    return mixer.blend(User)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_manage_user_view_unauthenticated(api_client):
    url = reverse('user:manage')

    # Test GET request
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Test PUT request
    data = {'username': 'newuser'}
    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
