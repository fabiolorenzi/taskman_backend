from django.db import models

class Task(models.Model):
    number = models.IntegerField(null = False)
    title = models.CharField(null = False, max_length = 50)
    description = models.TextField(null = False, max_length = 500)
    type = models.CharField(null = False, max_length = 10)
    priority = models.IntegerField(null = False)
    status = models.CharField(null = False, max_length = 20)
    project = models.IntegerField(null = False)
    user = models.IntegerField(null = False)
    iteration = models.IntegerField(null = False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    updated_by = models.IntegerField()