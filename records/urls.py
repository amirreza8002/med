from django.urls import path

from .views import (
    AllConditionListView,
    ConditionDetailView,
    ConditionCreateView,
    ConditionDeleteView,
    ConditionUpdateView,
    MedicineDelete,
    UserRecordListView,
    ConditionInfoDetail,
)

# app_name = "records"

urlpatterns = [
    path("condition/create/", ConditionCreateView.as_view(), name="condition_create"),
    path("patient/profile/", UserRecordListView.as_view(), name="patient_records"),
    path(
        "condition/detail/<int:pk>/",
        ConditionDetailView.as_view(),
        name="condition_detail",
    ),
    path(
        "condition/delete/<int:pk>/",
        ConditionDeleteView.as_view(),
        name="condition_delete",
    ),
    path(
        "condition/update/<int:pk>/",
        ConditionUpdateView.as_view(),
        name="condition_update",
    ),
    path(
        "condition/detail/<int:con_pk>/delete/<slug:medicine>/",
        MedicineDelete.as_view(),
        name="medicine_delete",
    ),
    path("conditions/list/", AllConditionListView.as_view(), name="all_conditions"),
    path(
        "condition/<slug:condition>/info/",
        ConditionInfoDetail.as_view(),
        name="condition_info",
    ),
]
