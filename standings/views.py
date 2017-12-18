from bs4 import BeautifulSoup as BS
from requests import get

from django.contrib.auth.decorators import login_required
from django.db import models
from django.shortcuts import get_object_or_404, render, redirect, reverse

from datetime import datetime
from pytz import utc

from .models import Owner, Team


def standings(request):
    message = ''
    if request.method == "POST":
        if request.POST.get('password') == 'reinhard':
            s = lambda l: BS(get(f'http://www.espn.com/soccer/standings/_/league/{l}.1').text, "html.parser")
            leagues = ['fra', 'ger', 'ita', 'esp', 'eng']
            now = datetime.now(utc)
            for league in leagues:
                soup = s(league)
                for club in soup.find_all(class_="standings-row"):
                    team, created = Team.objects.get_or_create(name=club.find(class_='team-names').text, league=league)
                    if created or (now - team.updated).total_seconds() > 60*60*4:
                        tds = club.find_all('td')
                        team.wins = tds[2].text
                        team.draws = tds[3].text
                        team.losses = tds[4].text
                        team.goal_diff = tds[7].text
                        team.save()
            return redirect('standings:standings')
        else:
            message = 'Please enter the correct password'
    owners = Owner.objects.annotate(
        score=models.Sum('teams__wins')*3+models.Sum('teams__draws'),
        goal_diff=models.Sum('teams__goal_diff')
    ).order_by('-score', '-goal_diff')
    return render(request, 'standings/standings.html', {'message': message, 'owners': owners})

def owner_page(request, pk):
    owner = get_object_or_404(Owner, pk=pk)
    teams = Team.objects.annotate(
        score=models.F('wins')*3+models.F('draws')
    ).order_by('-score', '-goal_diff')
    teams_you = teams.filter(owner=owner)
    teams_none = teams.filter(owner=None)
    return render(request, 'standings/owner.html', {'teams_you': teams_you, 'teams_none': teams_none, 'owner': owner})

def manage(request, pk):
    owner = get_object_or_404(Owner, pk=pk)
    if request.method == "POST":
        post = request.POST.dict()
        post.pop('csrfmiddlewaretoken')
        if post.pop('password') == 'reinhard':
            for key in post:
                team = get_object_or_404(Team, pk=key[1:])
                if team.owner == owner:
                    team.owner = None
                elif team.owner == None:
                    team.owner = owner
                team.save()
    return redirect(owner)
