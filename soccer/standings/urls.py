from django.urls import path

from . import views

app_name = 'standings'
urlpatterns = [
    path('', views.standings, name='standings'),
    path('<int:pk>/', views.owner_page, name='owner'),
    path('<int:pk>/add/<int:team_pk>', views.add, name='add'),
    path('<int:pk>/drop/<int:team_pk>', views.drop, name='drop'),
]
