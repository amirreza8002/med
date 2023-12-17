from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Medicine(models.Model):
    medicine = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.medicine

    def __repr__(self):
        return f"Medicine(medicine={self.medicine}, description={self.description if self.description else None})"


class ConditionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().values_list("condition", flat=True)


class ConditionInfo(models.Model):
    condition = models.CharField(max_length=255)
    info = models.TextField(null=True, blank=True)

    objects = models.Manager()
    all_conditions = ConditionManager()

    def __str__(self):
        return self.condition

    def __repr__(self):
        return f"ConditionInfo(condition={self.condition}, info={self.info})"

    def get_absolute_url(self):
        return reverse("condition_info", args=[str(self.id)])


class Condition(models.Model):
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    conditions = models.ForeignKey(
        ConditionInfo, on_delete=models.CASCADE, related_name="condition_info"
    )
    severity = models.CharField(max_length=100, blank=True, null=True)
    medicine = models.ManyToManyField(Medicine)
    MRI = models.ImageField(verbose_name=_("MRI image"), null=True, blank=True, max_length=255)

    objects = models.Manager()
    all_conditions = ConditionManager()

    def __str__(self):
        return self.conditions.condition

    def __repr__(self):
        return (
            f"Condition(condition={self.conditions}, "
            f"severity={self.severity if self.severity else None}, "
            f"medicine={self.medicine if self.medicine else None}, "
            f"descriptions={[desc for desc in self.descriptions.all()] if self.descriptions else None})"
        )

    def get_absolute_url(self):
        return reverse("condition_detail", args=[str(self.id)])


class InLineDescription(models.Model):
    description = models.TextField(blank=True, null=True)
    condition = models.ForeignKey(
        Condition, on_delete=models.CASCADE, related_name="descriptions"
    )

    def __repr__(self):
        return f"InLineDescription(description={self.description}, condition={self.condition.condition})"
