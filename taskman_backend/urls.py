from django.contrib import admin
from django.urls import path
from .views import sessions, users
from settings_data import environment

if environment == "Development":
    adminPath = admin.site.urls
else:
    adminPath = {}

urlpatterns = [
    path("api/v1/sessions", sessions.all_sessions),
    path("api/v1/sessions/single", sessions.single_session),
    path("api/v1/users", users.all_users)
]