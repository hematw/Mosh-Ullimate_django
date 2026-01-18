from django.urls import path
from .views import gyms_view, amenties_view

urlpatterns = [
    path("gyms", gyms_view),
    path("amenties/", amenties_view),
]
