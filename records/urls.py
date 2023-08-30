from django.urls import path

from .views import ConditionCreateView, UserProfileListView, ConditioDetailView

app_name = "records"

urlpatterns = [
    path("condition/create/", ConditionCreateView.as_view(), name="condition_create"),
    path("user/profile/", UserProfileListView.as_view(), name="user_profile"),
    path("condition/detail/<int:pk>/", ConditioDetailView.as_view(), name="condition_detail"),
]
