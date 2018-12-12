from django.apps import AppConfig
from server.Vault import Vault
from server.Logger import Colors


class ServerConfig(AppConfig):
    name = 'server'

    def ready(self):
        import server.signals # Used to import the signals
        print("\n\n"+Colors.OKGREEN)
        print("##########################################################")
        print("##\t\t\t\t\t\t\t##")
        print("##\t\tSIRS PROJECT - GROUP A43\t\t##")
        print("##\t\t\t\t\t\t\t##")
        print("##\t\tAuthors:\t\t\t\t##")
        print("##\t\t - Daniel Oliveira\t\t\t##")
        print("##\t\t - Pedro Cipriano\t\t\t##")
        print("##\t\t\t\t\t\t\t##")
        print("##########################################################")
        print(Colors.ENDC)

        Vault.load()
