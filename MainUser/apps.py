from django.apps import AppConfig


class MainuserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MainUser'

    def ready(self):
        import MainUser.signals