from django.contrib import admin
from django.db.models import F, Sum

from .models import Owner, Team

class OwnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'score')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(
            score=Sum('teams__wins')*3+Sum('teams__draws')+Sum('teams__goal_diff')
        )
        return qs

    def score(self, obj):
        return obj.score

    score.admin_order_field = "-score"

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'league', 'record', 'goal_diff', 'points', 'score')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(
            points=F('wins')*3+F('draws'),
            score=F('wins')*3+F('draws')+F('goal_diff')
        )
        return qs

    def points(self, obj):
        return obj.points

    def score(self, obj):
        return obj.score

    def goal_diff(self, obj):
        return obj.goal_diff

    points.admin_order_field = "-points"
    score.admin_order_field = "-score"
    goal_diff.admin_order_field = "-goal_diff"

    def get_ordering(self, request):
        return ['-score']

admin.site.register(Owner, OwnerAdmin)
admin.site.register(Team, TeamAdmin)
