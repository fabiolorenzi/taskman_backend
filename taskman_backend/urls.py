from django.contrib import admin
from django.urls import path
from .views import projects, sessions, teams, users
from settings_data import environment

if environment == "Development":
    adminPath = admin.site.urls
else:
    adminPath = {}

urlpatterns = [
    path("api/v1/projects", projects.all_projects),
    path("api/v1/projects/<int:id>", projects.single_project),
    path("api/v1/sessions", sessions.all_sessions),
    path("api/v1/sessions/single", sessions.single_session),
    path("api/v1/teams", teams.all_teams),
    path("api/v1/teams/<int:id>", teams.single_team),
    path("api/v1/users", users.all_users),
    path("api/v1/users/<int:id>", users.single_user)
]