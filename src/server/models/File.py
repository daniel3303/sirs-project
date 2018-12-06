from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac

import base64

from django.db import models
from server.models.User import User


class File(models.Model):
    class FileCorruptedException(Exception):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.content is None:
            self.setContent("")
        self.checkIntegrity()


    # The file name
    name = models.CharField(max_length=264)

    # The owner of the file
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')

    # The file's content
    content = models.BinaryField()

    # File's AES256 encryption key
    key = models.BinaryField(max_length=32, default=Fernet.generate_key())

    # File's HMAC
    mac = models.BinaryField(max_length=64)

    def getId(self):
        return self.id


    def getName(self):
        return self.name

    def setName(self, newName):
        self.name = newName
        self.updateMAC()

    def getOwner(self):
        return self.owner

    def setOwner(self, newOwner):
        self.owner = newOwner
        self.updateMAC()

    def getKey(self):
        return self.key

    def getContent(self):
        return self.decrypt(self.content)

    def setContent(self, newContent):
        self.content = self.encrypt(newContent)
        self.updateMAC()

    def encrypt(self, content):
        fernet = Fernet(self.key)
        contentToken = fernet.encrypt(content.encode("utf-8"))
        return contentToken

    def decrypt(self, content):
        fernet = Fernet(self.key)
        content = fernet.decrypt(self.content).decode("utf-8")
        return content

    def updateMAC(self):
        h = hmac.HMAC(self.key, hashes.SHA512(), backend=default_backend())
        h.update(self.content)
        self.mac = h.finalize()

    def save(self, *args, **kwargs):
        self.updateMAC()
        super().save(*args, **kwargs)

    def checkIntegrity(self):
        try:
            h = hmac.HMAC(self.key, hashes.SHA512(), backend=default_backend())
            h.update(self.content)
            h.verify(self.mac)
        except Exception as ex:
            raise File.FileCorruptedException("O ficheiro " + str(self.name)+" está corrompido. A assinatura é diferente do digest.")
