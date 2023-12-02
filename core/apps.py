from django.apps import AppConfig


class centroConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'


class TuAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        import custom_filters