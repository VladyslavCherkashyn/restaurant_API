import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


@pytest.fixture
def user_data():
    return {
        "email": "test@example.com",
        "password": "testpass",
        "first_name": "John",
        "last_name": "Doe",
    }


def test_create_superuser_without_is_staff(user_data):
    user_data["is_staff"] = False
    with pytest.raises(ValueError):
        User.objects.create_superuser(**user_data)


def test_create_superuser_without_is_superuser(user_data):
    user_data["is_superuser"] = False
    with pytest.raises(ValueError):
        User.objects.create_superuser(**user_data)
