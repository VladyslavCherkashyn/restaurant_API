import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from app.models import Restaurant, Menu, Vote


@pytest.fixture
def user():
    User = get_user_model()
    return User.objects.create_user(username='testuser', password='testpass', email='test@example.com')


@pytest.fixture
def restaurant():
    return Restaurant.objects.create(name='Restaurant 1', address='Address 1', chief_full_name='Chief 1')


@pytest.fixture
def menu(restaurant):
    menu_file = SimpleUploadedFile('menu.pdf', b'menu content')
    return Menu.objects.create(restaurant=restaurant, date='2023-01-01', menu=menu_file)


@pytest.fixture
def vote(user, menu):
    return Vote.objects.create(employee=user, menu=menu)


@pytest.mark.django_db
def test_restaurant_model(restaurant):
    assert restaurant.name == 'Restaurant 1'
    assert restaurant.address == 'Address 1'
    assert restaurant.chief_full_name == 'Chief 1'


@pytest.mark.django_db
def test_restaurant_str(restaurant):
    assert str(restaurant) == 'Restaurant 1: Address 1'



