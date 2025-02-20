from django.db import models

class Team(models.Model):
    user = models.IntegerField(null = False)
    role = models.CharField(null = False, max_length = 30)
    project = models.IntegerField(null = False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()