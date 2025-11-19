from django.apps import AppConfig


class WebservicesConfig(AppConfig):
    name = 'webservices'
    def ready(self):
       from BetfairUpdater import updater
       from soccer import soccerupdate
       updater.start()
       soccerupdate.start()