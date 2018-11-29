import importlib
from Logger import ConsoleLogger

class Kernel:
    logger = ConsoleLogger()

    # Register service providers here
    services = [
        "DatabaseServiceProvider",
        "EncryptUserPasswordServiceProvider",
        "EventLoggerServiceProvider",
    ]

    # Service instances
    instances = {

    }

    booted = False

    @staticmethod
    def boot():
        Kernel.logger.info("Kernel is booting services...")
        for service in Kernel.services:
            module = importlib.import_module("services."+service)
            class_ = getattr(module, service)
            serviceInstance = class_()
            serviceInstance.boot()
            Kernel.instances[service] = serviceInstance
            Kernel.logger.info("Booting service: "+service)

        Kernel.booted = True
        Kernel.logger.info("All services were booted...")

    @staticmethod
    def getService(service):
        if(Kernel.booted == False):
            exit("Kernel not booted")

        return Kernel.instances[service]
