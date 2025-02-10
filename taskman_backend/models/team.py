from django.db import models

class Team(models.Model):
    id = models.IntegerField(null = False, unique = True, primary_key = True)
    user = models.IntegerField(null = False)
    role = models.CharField(null = False)
    project = models.IntegerField(null = False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()