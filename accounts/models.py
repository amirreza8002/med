from autoslug import AutoSlugField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    name = models.CharField(_("Name of user"), max_length=255)
    email = models.EmailField(_("email address"), unique=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    slug = AutoSlugField(populate_from="username", unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)

    def get_absolute_url(self):
        return reverse("patient_records")
