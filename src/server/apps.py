from django.apps import AppConfig


class ServerConfig(AppConfig):
    name = 'server'

    def ready(self):
        import server.signals # Used to import the signals
