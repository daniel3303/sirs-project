from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.asymmetric import padding

from django.db import models

from server.Vault import Vault
from server.models.User import User


class File(models.Model):
    class FileCorruptedException(Exception):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # On object creation
        if self.content is None:
            self.key = File.generateFernetKey()
            self.setContent("")


    # The file name
    name = models.CharField(max_length=264)

    # The owner of the file
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')

    # The file's content
    content = models.BinaryField(default=None)

    # File's AES256 encryption key
    key = models.BinaryField(max_length=32, default=None)

    # File's HMAC
    mac = models.BinaryField(max_length=64, default=None)

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


    def getContent(self):
        return self.decrypt(self.content)

    def setContent(self, newContent):
        self.content = self.encrypt(newContent)
        self.updateMAC()

    def encrypt(self, content):
        fernet = Fernet(self.getDecryptedKey())
        contentToken = fernet.encrypt(content.encode("utf-8"))
        return contentToken

    def decrypt(self, content):
        fernet = Fernet(self.getDecryptedKey())
        content = fernet.decrypt(self.content).decode("utf-8")
        return content

    def getBytesForMAC(self):
        try:
            owner = self.owner.getId()
        except File.owner.RelatedObjectDoesNotExist as ex:
            owner = 0

        return  self.content + str(owner).encode("utf-8") + self.name.encode("utf-8") + self.key


    def updateMAC(self):
        h = hmac.HMAC(self.getDecryptedKey(), hashes.SHA512(), backend=default_backend())
        h.update(self.getBytesForMAC())
        self.mac = h.finalize()

    def save(self, *args, **kwargs):
        self.updateMAC()
        super().save(*args, **kwargs)

    def checkIntegrity(self):
        try:
            h = hmac.HMAC(self.getDecryptedKey(), hashes.SHA512(), backend=default_backend())
            h.update(self.getBytesForMAC())
            h.verify(self.mac)
        except Exception as ex:
            raise File.FileCorruptedException("O ficheiro " + str(self.name)+" está corrompido. A assinatura é diferente do digest.")

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
