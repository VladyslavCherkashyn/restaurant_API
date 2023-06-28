import pytest
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from mixer.backend.django import mixer
from rest_framework.request import RequestFactory
from app.models import Restaurant, Menu, Vote
from app.serializers import (
    CreateRestaurantSerializer,
    UploadMenuSerializer,
    RestaurantListSerializer,
    MenuListSerializer,
    ResultMenuListSerializer,
    VoteCreateSerializer,
)


@pytest.fixture
def menu():
    return mixer.blend(Menu)


@pytest.fixture
def user():
    return mixer.blend('auth.User')


@pytest.mark.django_db
def test_create_restaurant_serializer():
    serializer = CreateRestaurantSerializer(data={'name': 'Restaurant 1', 'address': '123 Main St'})
    assert serializer.is_valid()
    restaurant = serializer.save()
    assert restaurant.name == 'Restaurant 1'
    assert restaurant.address == '123 Main St'


@pytest.mark.django_db
def test_restaurant_list_serializer():
    restaurant = mixer.blend(Restaurant)
    serializer = RestaurantListSerializer(restaurant)
    assert serializer.data['name'] == restaurant.name
    assert serializer.data['address'] == restaurant.address




