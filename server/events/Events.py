class Events:
    #events
    userBeforeCreatedEventObservers = []

    @staticmethod
    def getBeforeUserCreatedEventObservers():
        return Events.userBeforeCreatedEventObservers

    @staticmethod
    def listenToBeforeUserCreated(observer):
        Events.userBeforeCreatedEventObservers.append(observer)
