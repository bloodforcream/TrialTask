# Generated by Django 2.2.7 on 2020-04-15 16:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Application name')),
                ('key', models.CharField(max_length=255, unique=True, verbose_name='Unique API key')),
                ('users', models.ManyToManyField(related_name='applications', to=settings.AUTH_USER_MODEL, verbose_name='Users allowed to use this application')),
            ],
        ),
    ]