from django.urls import path

from . import views

app_name = 'standings'
urlpatterns = [
    path('', views.standings, name='standings'),
    path('<int:pk>/', views.owner_page, name='owner'),
    path('<int:pk>/manage/', views.manage, name='manage'),
]
