from django.urls import path

from schmintroles.models import Roles
from . import views

urlpatterns = [
    path('api/roles', views.RolesAPI.as_view()),
    path('api/roles/<slug:id>', views.RolesAPI.as_view())
]