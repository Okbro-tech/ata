from django.apps import AppConfig
from django.apps import apps

class FeedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'feed'


def my_view(request):
    Subscription = apps.get_model('feed', 'Subscription')  # 'feed' is the app name
    # Your logic here


class FeedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'feed'

    def ready(self):
        import feed.signals  # Import signals here
