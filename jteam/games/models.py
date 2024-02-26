from django.conf import settings
from django.db import models
from django.utils import timezone


class Game(models.Model):
    CHOICES = (
        ('football', 'футбол'),
        ('tennis', 'теннис'),
        ('bowling', 'боулинг'),
    )

    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name="game_created",
                               on_delete=models.CASCADE)
    sport = models.CharField(max_length=255, choices=CHOICES)
    amount_players = models.PositiveIntegerField(default=2)
    place = models.CharField(max_length=255)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    duration = models.DurationField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return f'{self.sport} {self.date} {self.time} {self.place}'
