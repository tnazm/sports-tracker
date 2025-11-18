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
    path('account/update/', views.update_account, name='update_account'),
    path('account/delete/', views.delete_account, name='delete_account'),
    path('pick-team/', views.pick_team, name='pick_team'),
    path('favteamgames/<str:team>/',views.fav_team_games,name="fav_team_games")
    #path('teams/', views.teams, name='teams'),
    # path('refresh/', views.refresh_scores, name='refresh_scores'),
    # path("admin-dashboard/", views.admin_dashboard, name="dashboard"),
]

# Was for testing adding fav teams

# from sportstracker_app.models import Profile
# # Profile.objects.all().update(favorite_team={"fav_teams":[]})
# # count = Profile.objects.filter(favorite_team={"fav_teams":[]}).count()
# # print(f"Updated {count} profiles")

# Profile.objects.all().update(new=True)

# for profile in Profile.objects.all():
#     print(f"User: {profile.user.username}")
#     print(profile.new)
#     print(f"Bio: {profile.favorite_team}")
#     print("---")