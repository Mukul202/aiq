# Generated by Django 4.2.4 on 2023-08-09 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aiqAPI', '0002_powerplantmodel_statemodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='powerplantmodel',
            name='percentage',
        ),
    ]
