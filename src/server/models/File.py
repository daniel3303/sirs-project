from django.db import models

class File(models.Model):
    name = models.CharField(max_length=264)
