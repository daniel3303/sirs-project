import bcrypt
from services.ServiceProvider import ServiceProvider
from events.BeforeUserCreatedObserver import BeforeUserCreatedObserver
from events.Events import Events
from Logger import ConsoleLogger

class EncryptUserPasswordServiceProvider(ServiceProvider, BeforeUserCreatedObserver):
    def __init__(self):
        self.logger = ConsoleLogger()
        pass

    def boot(self):
        Events.listenToBeforeUserCreated(self)

    def onBeforeUserCreated(self, event):
        password = event.getPassword()
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf8'), salt)
        event.setPassword(str(hashed))
        self.logger.info("Encrypted user password for "+event.getUsername())
