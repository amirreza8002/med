from django.forms import ModelForm, TextInput

from .models import Condition, Medicine, ConditionInfo


class ConditionForm(ModelForm):
    class Meta:
        model = Condition
        exclude = ("patient", "medicine")
        widgets = {"medicine": TextInput(), "conditions": TextInput()}


class ConditionInputForm(ModelForm):
    class Meta:
        model = ConditionInfo
        fields = ("condition",)


class MedicineForm(ModelForm):
    class Meta:
        model = Medicine
        fields = ("medicine",)


class ConditionInfoForm(ModelForm):
    class Meta:
        model = ConditionInfo
        fields = ("condition",)
