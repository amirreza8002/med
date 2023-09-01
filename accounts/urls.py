from django.urls import include, path

from . import views

# app_name = "users"

urlpatterns = [
    path("", include("allauth.urls")),
    path("loggedout/", views.LoggedOut.as_view(), name="logged_out"),
    path("user/<str:username>/", views.UserDetailView.as_view(), name="user_detail"),
]
