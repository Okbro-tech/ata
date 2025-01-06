from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank_profile_picture.png')
    location = models.CharField(max_length=100, blank=True)
    subscriptions = models.ManyToManyField('self', symmetrical=False, related_name='subscribers', blank=True)

    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')  # Link to User model
    image = models.ImageField(upload_to="post_images", null=True, blank=True)
    caption = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    

    def __str__(self):
        return self.user.username

    
class Subscription(models.Model):
    subscriber = models.ForeignKey(User, related_name="subscriptions", on_delete=models.CASCADE)
    subscribed_to = models.ForeignKey(User, related_name="subscribers", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subscriber.username} -> {self.subscribed_to.username}"
  
def subscribe(subscriber_id, subscribed_to_id):
    try:
        # Dynamically load the Subscription model
        Subscription = apps.get_model('feed', 'Subscription')
        
        # Create a new subscription instance
        subscription = Subscription(
            subscriber_id=subscriber_id,
            subscribed_to_id=subscribed_to_id
        )
        
        # Save the subscription to the database
        subscription.save()
    except ObjectDoesNotExist:
        # Handle the case where the model or related objects do not exist
        print("The specified model or related objects do not exist.")
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")