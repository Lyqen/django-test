# Generated by Django 3.2.5 on 2024-10-31 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0005_auto_20241031_1510'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='busshift',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='busshift',
            name='start_time',
        ),
    ]
