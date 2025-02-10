import django

django.setup()
from .models import (
    project,
    session,
    task,
    team,
    user
)