# Generated by Django 2.0.1 on 2018-04-20 05:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0009_auto_20180420_0702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainunit',
            name='end_time_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='trainunit',
            name='start_time_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]