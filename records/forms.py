from django.forms import inlineformset_factory, ModelForm

from .models import Condition, InLineDescription


class ConditionForm(ModelForm):
    class Meta:
        model = Condition
        exclude = ("patient",)
