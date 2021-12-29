from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from profiles.api.views import ProfileViewSet, ProfileStatusViewSet, AvaterUpdateView

router = DefaultRouter()
router.register(r"profiles", ProfileViewSet)
router.register(r"status", ProfileStatusViewSet, basename="status")

# profile_list = ProfileViewSet.as_view({"get": "list"})
# profile_detail = ProfileViewSet.as_view({"get": "retrieve"})

urlpatterns = [
    path("", include(router.urls)),
    path("avater/", AvaterUpdateView.as_view(), name="avater-update"),
    # path("profiles/", profile_list, name="profile-list"),
    # path("profiles/<int:pk>/", profile_detail, name="profile-detail"),
]