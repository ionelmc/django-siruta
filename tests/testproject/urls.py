import pytest

from .views import DemoView

pytest.importorskip("django")

from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("rosetta/", include("rosetta.urls")),
    path("demo", DemoView.as_view(), name="demo"),
]
