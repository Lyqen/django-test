# Generated by Django 3.2.5 on 2024-10-31 14:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0004_auto_20241031_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='busshift',
            name='end_time',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AddField(
            model_name='busshift',
            name='start_time',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
    ]