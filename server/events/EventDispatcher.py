from events.Events import Events
from events.BeforeUserCreatedObserver import BeforeUserCreatedObserver
from Logger import ConsoleLogger

class EventDispatcher:
    logger = ConsoleLogger()

    def __init__(self):
        pass

    # Available events
    def fireBeforeUserCreatedEvent(self, username):
        for observer in Events.beforeUserCreatedEventObservers():
            if isinstance(observer, BeforeUserCreatedObserver) == False:
                EventDispatcher.logger.warning("Observer is not instance of BeforeUserCreatedObserver. Aborting...")
                exit()
            observer.onBeforeUserCreated(username)
