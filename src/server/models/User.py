from django.db import models

class User(models.Model):
    username = models.CharField(max_length=30)
    name = models.CharField(max_length=60)
    
