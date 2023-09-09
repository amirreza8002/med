from django.urls import path

from .views import AboutPage, HomePage, RobotsPage

# app_name = "pages"

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("about/", AboutPage.as_view(), name="about"),
    path("robots.txt", RobotsPage.as_view(content_type="text/plain"), name="robots"),
]
