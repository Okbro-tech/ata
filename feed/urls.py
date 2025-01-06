from django.urls import path, include
from . import views
from .views import delete_post, profile
urlpatterns = [
    path("", views.redirecthome, name='redirecthome'),
    path("home/", views.index, name='home'),
    path("signup/", views.signup, name='signup'),
    path("signin/", views.signin, name="signin"),
    path("logout/", views.logout, name="logout"),
    path("upload/", views.upload, name="upload"),
    path('profile/', views.profile, name='profile'),
    path('subscriptions/toggle/<int:user_id>/', views.toggle_subscription, name='toggle_subscription'),
    path('toggle_subscription/<int:user_id>/', views.toggle_subscription, name='toggle_subscription'),
    path('subscriptions/subscribe/<int:user_id>/', views.subscribe, name='subscribe'),
    path('profile/<int:user_id>/', views.profile, name='user_profile'),
    path('profile/<str:username>/', views.profile, name='profile_with_username'),  # Specific user's profile
    path('delete_post/<uuid:post_id>/', delete_post, name='delete_post'),
    path('profile/<int:user_id>/', profile, name='profile'),  # Make sure this exists
    
  ]




