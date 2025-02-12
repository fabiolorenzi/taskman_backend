from django.db import models

class Iteration(models.Model):
    project = models.IntegerField(null = False)
    version = models.CharField(null = False, max_length = 10)
    title = models.CharField(max_length = 100)
    description = models.TextField(max_length = 1000)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    updated_by = models.IntegerField(null = False)