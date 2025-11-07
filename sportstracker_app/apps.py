from django.apps import AppConfig


class SportstrackerAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sportstracker_app'



    def ready(self):
        import sportstracker_app.signals
