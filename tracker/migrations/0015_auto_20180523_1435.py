# Generated by Django 2.0.1 on 2018-05-23 12:35

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0014_auto_20180523_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True),
        ),
    ]
