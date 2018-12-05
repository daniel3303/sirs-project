from django.db import models
from server.models.User import User
from server.models.File import File

# Represents a User, a File and a set of permissions
class Role(models.Model):
    # The user
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # The file
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='editors')

    # The permissions
    read = models.BooleanField(default=False)
    write = models.BooleanField(default=False)

    def getId(self):
        return self.id

    def getOwner(self):
        return self.owner

    def getFile(self):
        return self.file

    def setFile(self, file):
        self.file = file

    def canRead(self):
        return self.read

    def canWrite(self):
        return self.write

    def setReadPermission(self, booleanValue):
        self.read = booleanValue

    def setWritePermission(self, booleanValue):
        self.write = booleanValue
