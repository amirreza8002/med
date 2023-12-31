from django.contrib import admin

from .models import Condition, ConditionInfo, InLineDescription, Medicine


class DescriptionInLine(admin.TabularInline):
    model = InLineDescription


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    model = Condition
    inlines = (DescriptionInLine,)


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    pass


@admin.register(ConditionInfo)
class ConditionInfoAdmin(admin.ModelAdmin):
    pass
