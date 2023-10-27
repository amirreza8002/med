from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from records.models import Condition, Medicine, ConditionInfo


class TestConditionCreateView(TestCase):
    User = get_user_model()

    @classmethod
    def setUpTestData(cls):
        cls.User.objects.create_user(
            username="amir",
            email="amir@email.com",
            password="testpass123",
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("condition_create"))

        assert response.status_code == 302

    def test_access_when_logged_in(self):
        self.client.login(email="amir@email.com", password="testpass123")
        response = self.client.get(reverse("condition_create"))

        assert response.status_code == 200

    def test_template_used(self):
        self.client.login(email="amir@email.com", password="testpass123")
        response = self.client.get(reverse("condition_create"))
        assert response.template_name[0] == "records/condition_create.html"

    def test_posting_to_create_view(self):
        self.client.login(email="amir@email.com", password="testpass123")

        respone = self.client.post(
            reverse(
                "condition_create",
            ),
            {"conditions": "headache", "severity": "low", "descriptions": "regular"},
        )

        assert respone.status_code == 302


class TestConditionDetailView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="amir",
            email="amir@email.com",
            password="testpass123",
        )
        cls.user2 = get_user_model().objects.create_user(
            username="reza",
            email="reza@email.com",
            password="testpass123",
        )

        cls.condition_info = ConditionInfo.objects.create(
            condition="cold"
        )

        cls.condition = Condition.objects.create(
            patient=cls.user,
            conditions=cls.condition_info,
            severity="mild",
        )

        cls.med = Medicine.objects.create(medicine="tea")
        cls.tea_med = Medicine.objects.filter(medicine="tea")
        cls.condition.medicines.set(cls.tea_med)
        cls.condition.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse("condition_detail", args=[int(self.condition.id)])
        )

        assert response.status_code == 302

    def test_access_denied_if_logged_in_as_different_user_than_the_patient(self):
        self.client.login(email="reza@email.com", password="testpass123")
        response = self.client.get(
            reverse("condition_detail", args=[int(self.condition.id)])
        )

        assert response.status_code == 403

    def test_access_when_logged_in_as_patient(self):
        self.client.login(email="amir@email.com", password="testpass123")
        response = self.client.get(
            reverse("condition_detail", args=[int(self.condition.id)])
        )

        assert response.status_code == 200

    def test_template_used(self):
        self.client.login(email="amir@email.com", password="testpass123")
        response = self.client.get(
            reverse("condition_detail", args=[int(self.condition.id)])
        )

        assert response.template_name[0] == "records/condition_detail.html"

    def test_page_contains_right_data(self):
        self.client.login(email="amir@email.com", password="testpass123")
        response = self.client.get(
            reverse("condition_detail", args=[int(self.condition.id)])
        )

        self.assertContains(response, "mild")


# TODO: ConditionDeleteView, ConditionUpdateView, MedicineDelete, UserRcordListView, AllConditionListView
