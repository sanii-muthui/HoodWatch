from django.apps import AppConfig

class HoodwatchConfig(AppConfig):
    name = 'hoodwatch'

    def ready (self):
        print('signal is ready')
        import hoodwatch.signals
