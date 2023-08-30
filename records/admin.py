from django.contrib import admin

from .forms import ConditionForm
from .models import Condition, InLineDescription


class DescriptionInLine(admin.TabularInline):
    model = InLineDescription


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    model = Condition
    inlines = (DescriptionInLine,)
