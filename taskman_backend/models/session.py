from django.db import models

class Session(models.Model):
    user = models.IntegerField(null = False, unique = True)
    passcode = models.CharField(null = False, unique = True, max_length = 50)
    expire = models.DateTimeField()