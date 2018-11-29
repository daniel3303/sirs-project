from services.ServiceProvider import ServiceProvider
from events.BeforeUserCreatedObserver import BeforeUserCreatedObserver
from events.Events import Events
from Logger import ConsoleLogger

class EventLoggerServiceProvider(ServiceProvider, BeforeUserCreatedObserver):
    def __init__(self):
        self.logger = ConsoleLogger()
        pass

    def boot(self):
        Events.listenToBeforeUserCreated(self)

    def onBeforeUserCreated(self, event):
        self.logger.success("New user created "+event.getUsername() + " with password " + event.getPassword())
