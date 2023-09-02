from django.urls import path

from .views import (ConditioDetailView, ConditionCreateView,
                    ConditionDeleteView, ConditionUpdateView,
                    UserProfileListView, MedicineDelete)

# app_name = "records"

urlpatterns = [
    path("condition/create/", ConditionCreateView.as_view(), name="condition_create"),
    path("patient/profile/", UserProfileListView.as_view(), name="patient_profile"),
    path(
        "condition/detail/<int:pk>/",
        ConditioDetailView.as_view(),
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
    path("condition/detail/<int:con_pk>/delete/<slug:medicine>/", MedicineDelete.as_view(), name="medicine_delete")
]
