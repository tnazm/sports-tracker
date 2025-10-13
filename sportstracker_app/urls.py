from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("", views.admin_dashboard, name="dashboard"),
    path('games/', views.games_page,name='games'),
]
