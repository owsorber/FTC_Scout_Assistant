from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('event/', views.event, name='event-info'),
    path('team/', views.team, name='team-page'),
    path('match-center/', views.matchCenter, name="match-center"),
    path('rankings/', views.rankings, name='rankings-page')
]