# Generated by Django 2.0.6 on 2018-09-10 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_tracker', '0007_auto_20180828_0716'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientconnection',
            name='rfid_tag',
        ),
        migrations.AddField(
            model_name='clientconnection',
            name='user',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='user'),
        ),
    ]
