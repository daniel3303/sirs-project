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
        pass

    def warning(self, message):
        pass

    def error(self, message):
        pass

    def info(self, message):
        pass

class ConsoleLogger(AbstractLogger):
    def __init__(self):
        pass

    def error(self, message):
        print(Colors.FAIL + "[ERROR]\t  " + str(message) + Colors.ENDC)

    def warning(self, message):
        print(Colors.WARNING + "[WARNING] " + str(message) + Colors.ENDC)

    def info(self, message):
        print(Colors.OKBLUE + "[INFO]\t  " + str(message) + Colors.ENDC)

    def success(self, message):
        print(Colors.OKGREEN + "[SUCCESS] " + str(message) + Colors.ENDC)
