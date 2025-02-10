from django.db import models

class User(models.Model):
    id = models.IntegerField(null = False, unique = True, primary_key = True)
    name = models.CharField(null = False, max_length = 20)
    surname = models.CharField(null = False, max_length = 20)
    email = models.EmailField(null = False)
    password = models.CharField(null = False, max_length = 99)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()