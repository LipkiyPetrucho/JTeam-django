# Generated by Django 5.0.2 on 2024-02-28 21:29

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={'ordering': ['-created_at'], 'verbose_name': 'Игра', 'verbose_name_plural': 'Игры'},
        ),
        migrations.RenameField(
            model_name='game',
            old_name='amount_players',
            new_name='max_players',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='time',
            new_name='start_time',
        ),
        migrations.RemoveField(
            model_name='game',
            name='author',
        ),
        migrations.RemoveField(
            model_name='game',
            name='created_date',
        ),
        migrations.AddField(
            model_name='game',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='joined_players',
            field=models.ManyToManyField(blank=True, related_name='joined_games', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='game',
            name='slug',
            field=models.SlugField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='game',
            name='status',
            field=models.CharField(choices=[('open', 'Open'), ('started', 'Started'), ('finished', 'Finished')], default='Open', max_length=255),
        ),
        migrations.AddField(
            model_name='game',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='Game',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='user_games_created',
                to=settings.AUTH_USER_MODEL
            )
        ),
        migrations.AddIndex(
            model_name='game',
            index=models.Index(fields=['-created_at'], name='games_game_created_1d9304_idx'),
        ),
    ]
