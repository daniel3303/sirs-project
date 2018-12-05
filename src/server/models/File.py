from django.db import models
from server.models.User import User

class File(models.Model):
    # The file name
    name = models.CharField(max_length=264)

    # The owner of the file
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')

    # The file's content
    content = models.TextField(default="")

    def getId(self):
        return self.id


    def getName(self):
        return self.name

    def setName(self, newName):
        self.name = newName

    def getOwner(self):
        return self.owner

    def setOwner(self, newOwner):
        self.owner = newOwner

    def getContent(self):
        return self.content

    def setContent(self, newContent):
        self.content = newContent
