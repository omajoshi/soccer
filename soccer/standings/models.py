from django.db import models
from django.shortcuts import reverse

from datetime import datetime
from pytz import utc

# Create your models here.
class Owner(models.Model):
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('standings:owner', args=[self.pk])

class Team(models.Model):
    FRA = 'fra'
    GER = 'ger'
    ITA = 'ita'
    ESP = 'esp'
    ENG = 'eng'
    LEAGUES = (
        (FRA, 'France'),
        (GER, 'Germany'),
        (ITA, 'Italy'),
        (ESP, 'Spain'),
        (ENG, 'England'),
    )
    name = models.CharField(max_length=100, blank=True)
    league = models.CharField(max_length=3, choices=LEAGUES, blank=True)
    goal_diff = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('Owner', on_delete=models.CASCADE, blank=True, null=True, related_name="teams")

    def __str__(self):
        return f'{self.name} of {self.league.upper()}'

    def record(self):
        return f'{self.wins}-{self.draws}-{self.losses}'
