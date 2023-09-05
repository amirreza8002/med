from django.urls import include, path

from . import views

# app_name = "users"

urlpatterns = [
    path("", include("allauth.urls")),
    path("loggedout/", views.LoggedOut.as_view(), name="logged_out"),
    path("user/<slug:slug>/", views.UserInfoUpdateView.as_view(), name="user_update"),
]
