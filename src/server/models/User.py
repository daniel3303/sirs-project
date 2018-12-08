from django.db import models
from django.contrib.auth.hashers import *


class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=256)
    name = models.CharField(max_length=60)

    def getId(self):
        return self.id

    def setUsername(self, username):
        self.username = username

    def getUsername(self):
        return self.username

    def setPassword(self, password):
        self.password = make_password(password)

    def getPassword(self):
        return self.password


    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    # Returns a file for which the user has read permissions
    def getFileForRead(self, id=0):
        try:
            file = self.files.get(id=id)
            return file
        except Exception as ex:
            pass

        for role in self.roles.all():
            if role.getFile().getId() == id:
                if role.canRead() == True:
                    return role.getFile()
                else:
                    return None

        return None
