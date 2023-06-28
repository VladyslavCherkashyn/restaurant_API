import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory
from mixer.backend.django import mixer
from app.models import Restaurant, Menu, Vote

from app.views import (
    VoteCreateView,
)


@pytest.fixture
def user():
    User = get_user_model()
    return User.objects.create_user(username='testuser', password='testpass')


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.fixture
def restaurant():
    return mixer.blend(Restaurant, name='Restaurant 1', address='Address 1', chief_full_name='Chief 1')


@pytest.fixture
def menu(restaurant):
    menu_file = SimpleUploadedFile('menu.pdf', b'menu content')
    return mixer.blend(Menu, restaurant=restaurant, date='2023-01-01', menu=menu_file)


@pytest.fixture
def vote(user, menu):
    return mixer.blend(Vote, employee=user, menu=menu)


@pytest.mark.django_db
def test_vote_create_view_anonymous_user(menu):
    view = VoteCreateView.as_view({'post': 'create'})
    request = RequestFactory().post('/votes/', {'menu_id': menu.id})
    request.user = AnonymousUser()
    response = view(request)
    assert response.status_code == 403
    assert Vote.objects.count() == 0
    assert menu.votes == 0
