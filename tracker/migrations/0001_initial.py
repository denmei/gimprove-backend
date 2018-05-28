# Generated by Django 2.0.1 on 2018-05-28 16:58

from django.conf import settings
import django.contrib.auth.mixins
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import tracker.models.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('name', models.CharField(help_text='Insert the name of the achievement here.', max_length=100, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, help_text='What did the user do to achieve it?', max_length=500, null=True)),
                ('achievement_image', models.ImageField(blank=True, null=True, upload_to=tracker.models.models.get_image_path)),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True, help_text='What kind of activity?', max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('description', models.CharField(help_text='Insert short description here.', max_length=1000)),
                ('gimprove_system', models.BooleanField(default=False)),
                ('equipment_machine', models.ManyToManyField(blank=True, help_text='Necessary equipment for the exercise.', to='tracker.Equipment')),
            ],
        ),
        migrations.CreateModel(
            name='ExerciseUnit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('time_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.Exercise')),
            ],
            options={
                'ordering': ['-time_date'],
            },
        ),
        migrations.CreateModel(
            name='GymProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('bio', models.TextField(blank=True, help_text='Beschreibung.', max_length=1000)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to=tracker.models.models.get_image_path)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Muscle',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='MuscleGroup',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('date_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('repetitions', models.IntegerField()),
                ('weight', models.FloatField()),
                ('durations', models.TextField(max_length=1200)),
                ('auto_tracking', models.BooleanField(default=False)),
                ('last_update', models.DateTimeField(default=django.utils.timezone.now)),
                ('exercise_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.ExerciseUnit')),
            ],
            options={
                'ordering': ['-date_time'],
            },
        ),
        migrations.CreateModel(
            name='TrainUnit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('start_time_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_time_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('date', models.DateField()),
            ],
            options={
                'ordering': ['-start_time_date'],
            },
            bases=(models.Model, django.contrib.auth.mixins.LoginRequiredMixin),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('bio', models.TextField(blank=True, help_text='Beschreibung.', max_length=1000)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to=tracker.models.models.get_image_path)),
                ('date_of_birth', models.DateField()),
                ('rfid_tag', models.CharField(blank=True, max_length=10, null=True, verbose_name='RFID')),
                ('_pr_active_set', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='tracker.Set')),
                ('achievements', models.ManyToManyField(blank=True, to='tracker.Achievement')),
                ('gym', models.ManyToManyField(blank=True, to='tracker.GymProfile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='trainunit',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.UserProfile'),
        ),
        migrations.AddField(
            model_name='muscle',
            name='muscle_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tracker.MuscleGroup'),
        ),
        migrations.AddField(
            model_name='gymprofile',
            name='members',
            field=models.ManyToManyField(blank=True, to='tracker.UserProfile'),
        ),
        migrations.AddField(
            model_name='exerciseunit',
            name='train_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.TrainUnit'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='muscles',
            field=models.ManyToManyField(help_text='Muscles trained by the exercise.', to='tracker.Muscle'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='exercises',
            field=models.ManyToManyField(to='tracker.Exercise'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='gym',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='gym', to='tracker.GymProfile'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='connection',
            name='followed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='connection',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activity',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='achievement',
            name='user',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
