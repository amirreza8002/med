from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Medicine(models.Model):
    medicine = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.medicine

    def __repr__(self):
        return f"Medicine(medicine={self.medicine}, description={self.description if self.description else None})"


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

    def __repr__(self):
        return (f"Condition(condition={self.condition}, "
                f"severity={self.severity if self.severity else None}, "
                f"medicine={self.medicines if self.medicines else None}, "
                f"descriptions={[desc for desc in self.descriptions.all()] if self.descriptions else None})")

    def get_absolute_url(self):
        return reverse("condition_detail", args=[str(self.id)])


class InLineDescription(models.Model):
    description = models.TextField(blank=True, null=True)
    condition = models.ForeignKey(
        Condition, on_delete=models.CASCADE, related_name="descriptions"
    )

    def __repr__(self):
        return f"InLineDescription(description={self.description}, condition={self.condition})"
