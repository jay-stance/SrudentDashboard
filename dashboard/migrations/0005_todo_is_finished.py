# Generated by Django 3.2.6 on 2021-09-06 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_rename_tod_todo'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='is_finished',
            field=models.BooleanField(default=False),
        ),
    ]
