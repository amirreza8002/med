from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Medicine(models.Model):
    medicine = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.medicine


class Condition(models.Model):
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="conditions"
    )
    condition = models.CharField(_("name of the condition"), max_length=255)
    severity = models.CharField(max_length=100, blank=True, null=True)
    medicines = models.ManyToManyField(
        Medicine, related_name="conditions", null=True, blank=True
    )

    def __str__(self):
        return self.condition

    def get_absolute_url(self):
        return reverse("condition_detail", args=[str(self.id)])


class InLineDescription(models.Model):
    description = models.TextField(blank=True, null=True)
    condition = models.ForeignKey(
        Condition, on_delete=models.CASCADE, related_name="descriptions"
    )
