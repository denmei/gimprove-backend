# Generated by Django 2.0.1 on 2018-05-23 18:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0016_auto_20180523_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
