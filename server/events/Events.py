class Events:
    #events
    userCreatedEventObservers = []

    @staticmethod
    def getUserCreatedEventObservers():
        return Events.userCreatedEventObservers

    @staticmethod
    def listenToUserCreated(observer):
        Events.userCreatedEventObservers(observer)
