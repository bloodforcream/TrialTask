from django.core.management.base import BaseCommand

from core.models import Application


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument('old_key', type=str)

    def handle(self, *args, **options):
        old_key = options['old_key']

        try:
            app = Application.objects.get(key=old_key)
        except Application.DoesNotExist:
            return 'Такого приложения не существует'

        app.regenerate_key()

        return f'Новый ключ: {app.key}'
