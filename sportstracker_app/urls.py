from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("week 1",views.week1, name="week1"),
    path("week 2",views.week2, name="week2"),
    path("week 3",views.week3, name="week3"),
    path("week 4",views.week4, name="week4"),
    path("week 5",views.week5, name="week5"),
    path("week 6",views.week6, name="week6"),
    path("week 7",views.week7, name="week7"),
    path("week 8",views.week8, name="week8"),
    path("week 9",views.week9, name="week9"),
    path("week 10",views.week10, name="week10"),
    path("week 11",views.week11, name="week11"),
    path("week 12",views.week12, name="week12"),
    path("week 13",views.week13, name="week13"),
    path("week 14",views.week14, name="week14"),
    path("week 15",views.week15, name="week15"),
    path("week 16",views.week16, name="week16"),
    path("week 17",views.week17, name="week17"),
    path("week 18",views.week18, name="week18"),
    # path("admin-dashboard/", views.admin_dashboard, name="dashboard"),
]
