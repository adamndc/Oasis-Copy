# Generated by Django 3.1.7 on 2021-04-27 00:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0011_report'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='date_added',
            new_name='date_reported',
        ),
    ]