from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    name = models.CharField(_("Name of user"), max_length=255)
    first_name = None
    last_name = None
    email = models.EmailField(_("email address"), unique=True)
    age = models.PositiveSmallIntegerField()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "age"]

    def get_absolute_url(self):
        return reverse("users:user_detail", kwargs={"username": self.username})
