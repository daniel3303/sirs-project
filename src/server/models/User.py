from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.asymmetric import padding

from django.db import models
from django.contrib.auth.hashers import *

from server.Vault import Vault


class User(models.Model):
    class UserCorruptedException(Exception):
        pass

    # Username for authentication
    username = models.CharField(max_length=30, unique=True, default="")

    # Password for authentication
    password = models.CharField(max_length=256, default="")

    # Personal name
    name = models.CharField(max_length=60, default="")

    # User's AES256 encryption key
    key = models.BinaryField(max_length=32, default=None)

    # User's HMAC
    mac = models.BinaryField(max_length=64, default=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # If we are creating the model then we should generate a random encryptation key
        if(self._state.adding == True and self.key == None):
            self.key = User.generateFernetKey()

    def getId(self):
        return self.id

    def setUsername(self, username):
        self.username = username
        self.updateMAC()

    def getUsername(self):
        return self.username

    def setPassword(self, password):
        self.password = make_password(password)
        self.updateMAC()

    def getPassword(self):
        return self.password


    def setName(self, name):
        self.name = name
        self.updateMAC()

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

    # Returns a file for which the user has write permissions
    def getFileForWrite(self, id=0):
        try:
            file = self.files.get(id=id)
            return file
        except Exception as ex:
            pass

        for role in self.roles.all():
            if role.getFile().getId() == id:
                if role.canWrite() == True:
                    return role.getFile()
                else:
                    return None

        return None

    # Methods related to model integrity
    def getDecryptedKey(self):
        key = Vault.getPrivateKey().decrypt(
            self.key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return key

    def getBytesForMAC(self):
        return (str(self.id) + str(self.name) + str(self.username) + str(self.password) + str(self.key)).encode("utf-8")


    def updateMAC(self):
        h = hmac.HMAC(self.getDecryptedKey(), hashes.SHA512(), backend=default_backend())
        h.update(self.getBytesForMAC())
        self.mac = h.finalize()

    def save(self, *args, **kwargs):
        # If the model is new then we insert it to generate an id
        # then we compute the MAC using the id and then we save the model again
        if(self._state.adding == True):
            super().save(*args, **kwargs)
            self.updateMAC()
            super().save(*args, **kwargs)
        else:
            self.updateMAC()
            super().save(*args, **kwargs)

    def checkIntegrity(self):
        try:
            h = hmac.HMAC(self.getDecryptedKey(), hashes.SHA512(), backend=default_backend())
            h.update(self.getBytesForMAC())
            h.verify(self.mac)
        except Exception as ex:
            raise User.UserCorruptedException("O utilizador " + str(self.username)+" está corrompido. A assinatura é diferente do digest.")

    def isCorrupted(self):
        try:
            self.checkIntegrity()
            return False
        except Exception as ex:
            return True

    @staticmethod
    def generateFernetKey():
        uncipheredKey = Fernet.generate_key()

        cipherKey = Vault.getPublicKey().encrypt(
            uncipheredKey,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return cipherKey
