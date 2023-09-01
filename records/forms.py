from django.forms import ModelForm

from .models import Condition


class ConditionForm(ModelForm):
    class Meta:
        model = Condition
        exclude = ("patient",)
