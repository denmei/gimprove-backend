# Generated by Django 2.0.1 on 2018-01-18 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0040_auto_20180118_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='set',
            name='weight',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='set',
            name='repetitions',
            field=models.IntegerField(default=0),
        ),
    ]