from django.test import SimpleTestCase
from django.urls import reverse


class RobotsTxtTests(SimpleTestCase):
    def test_get(self):
        response = self.client.get("/robots.txt")

        assert response.status_code == 200
        assert response["content-type"] == "text/plain"

    def test_template_used(self):
        response = self.client.get(reverse("robots"))

        assert response.template_name[0] == "robots.txt"


class HomePageTest(SimpleTestCase):
    def test_page_available(self):
        response = self.client.get("")

        assert response.status_code == 200

    def test_template_used(self):
        response = self.client.get(reverse("home"))

        assert response.template_name[0] == "home.html"
        self.assertContains(response, "Home")


class AboutPage(SimpleTestCase):
    def test_page_available(self):
        response = self.client.get(reverse("about"))

        assert response.status_code == 200

    def test_template_used(self):
        response = self.client.get(reverse("about"))

        assert response.template_name[0] == "about.html"
        self.assertContains(response, "About")
