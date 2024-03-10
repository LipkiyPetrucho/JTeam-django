# Generated by Django 5.0.2 on 2024-03-08 19:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_alter_game_slug'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={'ordering': ['created_at'], 'verbose_name': 'Игра', 'verbose_name_plural': 'Игры'},
        ),
        migrations.RemoveIndex(
            model_name='game',
            name='games_game_created_1d9304_idx',
        ),
        migrations.AlterField(
            model_name='game',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
        migrations.AddIndex(
            model_name='game',
            index=models.Index(fields=['created_at'], name='games_game_created_1f2afd_idx'),
        ),
    ]
