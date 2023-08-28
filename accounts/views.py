from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.views.generic import DetailView


class UserDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    slug_field = "username"


class LoggedOut(LogoutView):
    template_name = "account/logged_out.html"
