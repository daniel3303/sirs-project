from django.db import models
from server.models.User import User

# Represents a User, a File and a set of permissions
class Role(models.Model):
    # The user
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # The file
    file = models.CharField(max_length=264)

    # The permissions
    read = models.BooleanField(default=False)
    write = models.BooleanField(default=False)
