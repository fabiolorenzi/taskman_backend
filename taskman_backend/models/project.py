from django.db import models

class Project(models.Model):
    name = models.CharField(null = False, max_length = 100)
    description = models.TextField(max_length = 500)
    main_user = models.IntegerField(null = False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()