from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TestUserInfoView(TestCase):
    USER = get_user_model()

    @classmethod
    def setUpTestData(cls):
        cls.USER.objects.create_user(
            username="amir",
            email="amir@email.com",
            password="testpass123",
        )
        cls.USER.objects.create_user(
            username="reza", email="reza@email.com", password="testpass123"
        )

    def test_page_is_login_required(self):
        response = self.client.get(reverse("user_update", args=[str("amir")]))
        assert response.status_code == 302

        self.client.login(email="amir@email.com", password="testpass123")
        response = self.client.get(reverse("user_update", args=[str("amir")]))
        assert response.status_code == 200

    def test_template_used(self):
        self.client.login(email="amir@email.com", password="testpass123")
        response = self.client.get(reverse("user_update", args=[str("amir")]))

        assert response.template_name[0] == "account/user_update.html"

    def test_forbbiden_whhen_entering_another_users_page(self):
        self.client.login(email="amir@email.com", password="testpass123")
        response = self.client.get(reverse("user_update", args=[str("reza")]))
        assert response.status_code == 403

    def test_posting_to_update_view(self):
        self.client.login(email="amir@email.com", password="testpass123")
        respone = self.client.post(
            reverse("user_update", args=[str("amir")]),
            {"name": "amir", "email": "amir@email.com", "age": 21},
        )
        assert respone.status_code == 302
