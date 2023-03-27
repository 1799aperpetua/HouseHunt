from django.apps import AppConfig


class HouseLogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'house_log'

    def ready(self):
        import house_log.signals