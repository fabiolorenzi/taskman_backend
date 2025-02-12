import django

django.setup()
from .models import (
    iteration,
    project,
    session,
    task,
    team,
    user
)