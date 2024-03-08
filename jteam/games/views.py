from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import GameCreateForm
from .models import Game

def validate_date(value):
    if value < timezone.now().date():
        raise ValidationError('Дата не может быть в прошлом.')


def validate_time(value):
    now = timezone.now()
    if value < now.time() or (value == now.time() and now.date() > value.date()):
        raise ValidationError('Время не может быть в прошлом.')

@login_required
def game_create(request):
    if request.method == 'POST':
        form = GameCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_game = form.save(commit=False)
            new_game.user = request.user
            new_game.save()
            messages.success(request,
                             'Игра успешно создана')
            return redirect(new_game.get_absolute_url())
    else:
        form = GameCreateForm()
    return render(request,
                  'games/game/create.html',
                  {'section': 'games',
                   'form': form})


def game_detail(request, id, slug):
    game = get_object_or_404(Game, id=id, slug=slug)
    return render(request,
                  'games/game/detail.html',
                  {'section': 'games',
                   'game': game})

@login_required
def game_list(request):
    """Выводит постраничный список игр"""
    games = Game.objects.all()
    paginator = Paginator(games, 3)
    page_number = request.GET.get('page', 1)
    try:
        games = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page_number не целое число, то
        # выдать первую страницу
        games = paginator.page(1)
    except EmptyPage:
        # Если page_number находится вне диапозона, то
        # выдать последнюю страницу результатов
        games = paginator.page(paginator.num_pages)
    return render(request,
                  'games/game/list.html',
                  {"section": 'games',
                   'games': games})

# Не дает пользователям, не вошедшим в систему, обращаться к этому представлению.
# Этому представлению разрешаются запросы только методом POST.
@login_required
@require_POST
def game_join(request):
    """ Представление, которое позволяет пользователям присоед./выйти из игры"""
    game_id = request.POST.get('id')
    # action берется из атрибута action="/submit", если его нет, то есть ещё варианты.
    action = request.POST.get('action')
    if game_id and action:
        try:
            game = Game.objects.get(id=game_id)
            if action == 'join':
                # Проверяет лимит присоединений
                if game.joined_players.count() >= game.max_players:
                    messages.error(request,
                                     'Максимальное количество игроков достигнуто.')
                    return JsonResponse({'status': 'error',
                                         'message': 'Максимальное количество игроков достигнуто.'})
                # Добавление пользователя в игру
                game.joined_players.add(request.user)
            else:
                game.joined_players.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Game.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})
