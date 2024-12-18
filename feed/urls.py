from django.urls import path
from . import views
urlpatterns = [
    path("", views.redirecthome, name='redirecthome'),
    path("profile/", views.profile, name='profile'),
    path("home/", views.index, name='home'),
    path("signup/", views.signup, name='signup'),
    path("signin/", views.signin, name="signin"),
    path("logout/", views.logout, name="logout"),
    path("upload/", views.upload, name="upload"),
]
