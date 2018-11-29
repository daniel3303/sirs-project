import json
from Kernel import Kernel
from services.DatabaseServiceProvider import DatabaseServiceProvider
from Server import Server

class Application:
    config = {}
    def __init__(self):
        with open("config/application.json") as configFile:
            Application.config = json.loads(configFile.read())

        Kernel.boot()

        self.server = Server(Application.config["host"], Application.config["port"], Application.config["secureMode"])
        self.databaseServiceProvider = Kernel.getService("DatabaseServiceProvider")

    def start(self):
        self.server.start()
