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
