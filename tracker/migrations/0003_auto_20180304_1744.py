# Generated by Django 2.0.1 on 2018-03-04 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_auto_20180301_1558'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='_active_set',
            new_name='_pr_active_set',
        ),
    ]
