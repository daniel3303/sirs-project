from services.ServiceProvider import ServiceProvider
from events.EventDispatcher import EventDispatcher
from database.SQLiteDatabase import SQLiteDatabase
from events.BeforeUserCreatedEvent import BeforeUserCreatedEvent

class DatabaseServiceProvider(ServiceProvider):
    def __init__(self):
        self.driver = SQLiteDatabase()
        self.eventDispatcher = EventDispatcher()

    def createUser(self, username, password):
        event = BeforeUserCreatedEvent(username, password)

        # Receives the event after all services process it
        event = self.eventDispatcher.fireBeforeUserCreatedEvent(event)
        self.driver.createUser(event.getUsername(), event.getPassword())

    def getAllUsers(self):
        return self.driver.getAllUsers()
