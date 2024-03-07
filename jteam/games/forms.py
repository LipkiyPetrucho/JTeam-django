from django import forms
from .models import Game


class GameCreateForm(forms.ModelForm):
    """
    Форма создания игры.

    """

    class Meta:
        model = Game
        fields = [
            'sport',
            'place',
            'date',
            'start_time',
            'duration',
            'max_players',
            'price',
            'description',
        ]
        labels = {
            'sport': 'Вид спорта',
            'place': 'Место игры',
            'date': 'Дата игры',
            'start_time': 'Время начала игры',
            'duration': 'Продолжительность',
            'max_players': 'Количество игроков',
            'price': 'Цена игры',
            'description': 'Описание',
        }


