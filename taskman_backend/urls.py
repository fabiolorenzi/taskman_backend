from django.contrib import admin
from django.urls import path
from settings_data import environment

if environment == "Development":
    adminPath = admin.site.urls
else:
    adminPath = {}

urlpatterns = [
    path("admin/", adminPath)
]