from django.db import models
from server.models.User import User
from server.models.Role import Role

class File(models.Model):
    # The file name
    name = models.CharField(max_length=264)

    # The owner of the file
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # The other users with permissions to this file
    editors = models.ForeignKey(Role, on_delete=models.CASCADE)
