from django.apps import AppConfig


class ValidacionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'validacion'

    def ready(self):
        import validacion.signals