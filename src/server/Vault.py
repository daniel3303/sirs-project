from cryptography.hazmat.backends import default_backend
from cryptography import x509
from cryptography.hazmat.primitives import serialization

#FIXME clear memory on exit
class Vault:
    certificate = None
    privateKey = None

    @staticmethod
    def getPublicKey():
        return Vault.getCertificate().public_key()

    @staticmethod
    def getCertificate():
        if Vault.certificate is not None:
            return Vault.certificate
        else:
            with open("certificates/db-cert.pem", "rb") as certificateFile:
                Vault.certificate = x509.load_pem_x509_certificate(certificateFile.read(), default_backend())

            return Vault.certificate

    @staticmethod
    def getPrivateKey():
        if Vault.privateKey is None:
            with open("certificates/db-key.pem", "rb") as privateKeyFile:
                Vault.privateKey = serialization.load_pem_private_key(
                    privateKeyFile.read(),
                    password=b"8M@!Sa#XA&4A7PJF", #FIXME dynamically ask
                    backend=default_backend()
                )
                return Vault.privateKey
        else:
            return Vault.privateKey
