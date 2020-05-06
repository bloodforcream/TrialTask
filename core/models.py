from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models


class Application(models.Model):
    name = models.CharField(max_length=255, verbose_name='Application name')
    key = models.CharField(max_length=255, unique=True, verbose_name='Unique API key')

    def regenerate_key(self):
        self.key = str(uuid4())
        self.save()
