# Generated by Django 2.0.1 on 2018-08-27 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_tracker', '0002_auto_20180827_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='set',
            name='rfid',
            field=models.TextField(default='123', max_length=10),
            preserve_default=False,
        ),
    ]