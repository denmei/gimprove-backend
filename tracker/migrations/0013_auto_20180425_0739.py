# Generated by Django 2.0.1 on 2018-04-25 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0012_auto_20180424_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='set',
            name='weight',
            field=models.FloatField(),
        ),
    ]
