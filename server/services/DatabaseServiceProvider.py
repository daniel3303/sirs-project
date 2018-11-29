from services.ServiceProvider import ServiceProvider
from events.EventDispatcher import EventDispatcher

class DatabaseServiceProvider(ServiceProvider):
    def __init__(self):
        self.eventDispatcher = EventDispatcher()

    def createUser(username, password):
        EventDispatcher.fireBeforeUserCreatedEvent(username)
