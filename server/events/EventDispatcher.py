from events.Events import Events
from events.UserCreatedObserver import Events
from Logger import ConsoleLogger

class EventDispatcher:
    logger = ConsoleLogger()

    def __init__(self):
        pass

    # Available events
    def fireUserCreatedEvent(self, username):
        for observer in Events.userCreatedEventObservers():
            if isinstance(observer, UserCreatedObserver) == False:
                EventDispatcher.logger.warning("Observer is not instance of UserCreatedObserver. Aborting...")
                exit()
