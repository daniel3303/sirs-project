import json
from providers.DatabaseServiceProvider import DatabaseServiceProvider
from Server import Server

class Application:
    config = {}
    def __init__(self):
        with open("config/application.json") as configFile:
            Application.config = json.loads(configFile.read())
        self.databaseServiceProvider = DatabaseServiceProvider()
        self.server = Server(Application.config["host"], Application.config["port"], Application.config["secureMode"])


    def start(self):
        self.server.start()
