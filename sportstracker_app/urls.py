from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('week/<int:num>/', views.week, name='week'),
    path('newuserwelcome/',views.pick_team,name='pickteam'),
    path('account/',views.user_account,name='account'),
    path('pick-team/', views.pick_team, name='pick_team'),
    #path('teams/', views.teams, name='teams'),
    # path('refresh/', views.refresh_scores, name='refresh_scores'),
    # path("admin-dashboard/", views.admin_dashboard, name="dashboard"),
]
