from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LogoutView
from django.views.generic import UpdateView


class LoggedOut(LogoutView):
    template_name = "account/logged_out.html"


class UserInfoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = get_user_model()
    fields = ("name", "email", "age")
    template_name = "account/user_update.html"

    def test_func(self):
        obj = self.get_object()
        return obj == self.request.user
