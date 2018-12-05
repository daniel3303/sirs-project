from django.db import models
from server.models.User import User

class File(models.Model):
    # The file name
    name = models.CharField(max_length=264)

    # The owner of the file
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
