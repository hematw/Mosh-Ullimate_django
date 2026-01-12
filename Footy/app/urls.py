from django.urls import path
from .views import gyms_view

urlpatterns = [
    path("", gyms_view)
]
