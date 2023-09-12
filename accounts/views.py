from allauth.account.views import PasswordChangeView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView


class LoggedOut(LogoutView):
    template_name = "account/logged_out.html"


class UserInfoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = get_user_model()
    fields = ("name", "email", "age")
    template_name = "account/user_update.html"

    def test_func(self):
        obj = self.get_object()
        return obj == self.request.user


class PasswordChangeDone(TemplateView):
    template_name = "account/password_change_done.html"


class PasswordChangeViewCustom(PasswordChangeView):
    success_url = reverse_lazy("change_password_done")
