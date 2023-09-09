from django.contrib.auth import get_user_model
from django.test import TestCase


class TestConditionDetailView(TestCase):
    User = get_user_model()

    @classmethod
    def setUpTestData(cls):
        cls.User.objects.create(
            username="amir",
            email="amir@email.com",
            password="testpass123",
        )

    # TODO: test
