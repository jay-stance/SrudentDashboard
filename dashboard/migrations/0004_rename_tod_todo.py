# Generated by Django 3.2.6 on 2021-09-06 18:14

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0003_auto_20210906_1113'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tod',
            new_name='Todo',
        ),
    ]
