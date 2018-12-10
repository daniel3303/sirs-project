from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.asymmetric import padding

from django.db import models

from server.models.User import User
from server.models.File import File

# Represents a User, a File and a set of permissions
class Role(models.Model):
    class RoleCorruptedException(Exception):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # If the model is corrupted remove the permissions
        if(self._state.adding == False and self.isCorrupted() == True):
            self.setReadPermission(False)
            self.setWritePermission(False)


    # The user
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roles')

    # The file
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='editors')

    # The permissions
    read = models.BooleanField(default=False)
    write = models.BooleanField(default=False)

    # File's HMAC
    mac = models.BinaryField(max_length=64, default=None)

    class Meta:
        unique_together = (('user', 'file'),)

    def getId(self):
        return self.id

    def getUser(self):
        return self.user

    def setUser(self, user):
        self.user = user
        self.updateMAC()

    def getFile(self):
        return self.file

    def setFile(self, file):
        self.file = file
        self.updateMAC()

    def canRead(self):
        return self.read

    def canWrite(self):
        return self.write

    def setReadPermission(self, booleanValue):
        self.read = booleanValue
        self.updateMAC()

    def setWritePermission(self, booleanValue):
        self.write = booleanValue
        self.updateMAC()

    def getBytesForMAC(self):
        return  str(self.file.getId()).encode("utf-8") + str(self.user.getId()).encode("utf-8") + str(self.write).encode("utf-8") + str(self.read).encode("utf-8")

    def updateMAC(self):
        try:
            if(self.user is None or self.file is None):
                return
        except:
            return

        h = hmac.HMAC(self.file.getDecryptedKey(), hashes.SHA512(), backend=default_backend())
        h.update(self.getBytesForMAC())
        self.mac = h.finalize()

    def checkIntegrity(self):
        try:
            h = hmac.HMAC(self.getDecryptedKey(), hashes.SHA512(), backend=default_backend())
            h.update(self.getBytesForMAC())
            h.verify(self.mac)
        except Exception as ex:
            raise Role.RoleCorruptedException("A permissão " + str(self.id)+" está corrompida. A assinatura é diferente do digest.")

    def isCorrupted(self):
        try:
            self.checkIntegrity()
            return False
        except Exception as ex:
            return True

    def save(self, *args, **kwargs):
        self.updateMAC()
        super().save(*args, **kwargs)
