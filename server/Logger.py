class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class AbstractLogger:
    def __init__(self):


    def logWarning(self, message):

    def logError(self, message):

    def logInfo(self, message):


class ConsoleLogger(AbstractLogger):
    def __init__(self):

    def logWarning(self, message):
        print(Colors.WARNING + str(message) + Colors.ENDC)
