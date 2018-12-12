from cryptography.hazmat.backends import default_backend
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from server.Logger import ConsoleLogger
import getpass

#FIXME clear memory on exit
class Vault:
    certificate = None
    privateKey = None
    password = None

    @staticmethod
    def load():
        logger = ConsoleLogger()
        if(Vault.password is None):
            print("Type the password to decrypt the Vault.")
            print("For more information about this you can read the README.md file (section \"How to run\", subsection \"Quick note\").")
            print("If you type a wrong password the program will continue running but it won´t be able to decrypt any data.")
            logger.warning("The default password is: 8M@!Sa#XA&4A7PJF (we are printing it here just to save some time, we wouldn´t do this on a production enviroment)")
            Vault.password = getpass.getpass(prompt="RSA key decryption password:").encode("ASCII")

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
                    password=Vault.password,
                    backend=default_backend()
                )
                return Vault.privateKey
        else:
            return Vault.privateKey
