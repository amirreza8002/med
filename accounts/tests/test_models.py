from django.contrib.auth import get_user_model
from django.test import TestCase


class TestUserModel(TestCase):
    User = get_user_model()

    def test_create_user(self):
        user = self.User.objects.create_user(
            name="amir",
            username="amir",
            email="amir@email.com",
            age=21,
        )

        assert user.username == "amir"
        assert user.email == "amir@email.com"
        assert user.age == 21
        assert user.name == "amir"
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser

    def test_create_super_user(self):
        user = self.User.objects.create_superuser(
            username="superamir", email="superamir@email.com", password="testpass123"
        )

        assert user.username == "superamir"
        assert user.email == "superamir@email.com"
        assert user.is_active
        assert user.is_staff
        assert user.is_superuser
