# Generated by Django 3.1.7 on 2021-04-20 20:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pages', '0006_auto_20210419_1931'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='buyer',
            field=models.ForeignKey(default=2, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='buyer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='conversation',
            name='seller',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seller', to=settings.AUTH_USER_MODEL),
        ),
    ]