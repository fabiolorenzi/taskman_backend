from django.db import models

class Task(models.Model):
    id = models.IntegerField(null = False, unique = True, primary_key = True)
    number = models.IntegerField(null = False)
    title = models.CharField(null = False, max_length = 50)
    description = models.TextField(null = False, max_length = 500)
    type = models.CharField(null = False)
    priority = models.IntegerField(null = False, min = 1, max = 5)
    status = models.CharField(null = False)
    project = models.IntegerField(null = False)
    user = models.IntegerField(null = False)
    iteration = models.IntegerField(null = False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    updated_by = models.IntegerField()