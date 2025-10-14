from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('week/<int:num>/', views.week, name='week'),
    path('refresh/', views.refresh_scores, name='refresh_scores'),
    # path("admin-dashboard/", views.admin_dashboard, name="dashboard"),
]
