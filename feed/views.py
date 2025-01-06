from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, Subscription
from django.http import JsonResponse
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, auth
from django.http import HttpResponseForbidden

User = get_user_model()

def redirecthome(request):
    return redirect('home')

@login_required(login_url='signin')
def index(request):
    user_profile = Profile.objects.get(user=request.user)
    posts = Post.objects.all()
    return render(request, 'socialmedia.html', {'user_profile': user_profile, 'posts': posts})

def signup(request):
    if request.method == "POST":
        username, password, password2 = request.POST['username'], request.POST['password'], request.POST['password2']
        if password != password2:
            messages.info(request, 'Password not matching')
        elif User.objects.filter(username=username).exists():
            messages.info(request, "Username taken")
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            Profile.objects.create(user=user, id_user=user.id)
            return redirect('signin')
    return render(request, 'signup.html')

def signin(request):
    if request.method == "POST":
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user:
            login(request, user)
            return redirect("home")
        messages.info(request, "Invalid credentials")
    return render(request, 'signin.html')

@login_required(login_url='signin')
def logout_view(request):
    logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def profile(request, user_id=None):
    user = get_object_or_404(User, id=user_id) if user_id else request.user
    user_profile = Profile.objects.get(user=user)
    user_posts = Post.objects.filter(user=user)
    follower_count = Subscription.objects.filter(subscribed_to=user).count()
    return render(request, "profile.html", {
        "user_profile": user_profile, "user_posts": user_posts, 
        "follower_count": follower_count, "is_own_profile": request.user == user_profile.user
    })

@login_required(login_url='signin')
def upload(request):
    if request.method == "POST" and (image := request.FILES.get('image_upload')):
        Post.objects.create(user=request.user, image=image, caption=request.POST.get('caption', ''))
        messages.success(request, "Post uploaded successfully!")
    else:
        messages.error(request, "Image is required.")
    return redirect("/")

@login_required
def toggle_subscription(request, user_id):
    target_profile = get_object_or_404(Profile, user__id=user_id)
    current_profile = get_object_or_404(Profile, user=request.user)
    if request.user.id == user_id:
        return JsonResponse({"error": "Cannot subscribe to yourself."}, status=400)

    if target_profile in current_profile.subscriptions.all():
        current_profile.subscriptions.remove(target_profile)
        subscribed = False
    else:
        current_profile.subscriptions.add(target_profile)
        subscribed = True
    subscriber_count = target_profile.subscribers.count()
    return JsonResponse({'subscribed': subscribed, 'subscriber_count': subscriber_count})

@login_required(login_url='signin')
def subscribe(request, user_id):
    try:
        user_to_subscribe = User.objects.get(id=user_id)
        subscription, created = Subscription.objects.get_or_create(subscriber=request.user, subscribed_to=user_to_subscribe)
        if not created:
            subscription.delete()
        return redirect('profile')
    except User.DoesNotExist:
        return redirect('home')

def create_subscription(subscriber_id, subscribed_to_id):
    try:
        Subscription = apps.get_model('feed', 'Subscription')
        subscription, created = Subscription.objects.get_or_create(subscriber_id=subscriber_id, subscribed_to_id=subscribed_to_id)
        return created
    except ObjectDoesNotExist:
        print("Model or object not found.")
    except Exception as e:
        print(f"Error: {e}")

@login_required
def toggle_subscription_view(request, user_id):
    if request.method == "POST":
        if request.user.id == user_id:
            return JsonResponse({"error": "Cannot subscribe to yourself."}, status=400)
        try:
            created = create_subscription(request.user.id, user_id)
            return JsonResponse({"message": "Subscribed successfully." if created else "Unsubscribed successfully.", "subscribed": created})
        except Exception:
            return JsonResponse({"error": "An error occurred."}, status=500)
    return JsonResponse({"error": "Invalid request method."}, status=405)

def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(Profile, user=user)
    user_posts = Post.objects.filter(user=user)
    subscriber_count = user_profile.followers.count()
    context = {'user_profile': user_profile, 'user_posts': user_posts, 'subscriber_count': subscriber_count}
    return render(request, 'profile.html', context)

def profile_view(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        # Redirect to profile creation page or auto-create
        return redirect('create_profile')
    return render(request, 'profile.html', {'subscription_count': 0})

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

def create_superuser(self, email, first_name, last_name, username, date_of_birth, password, **kwargs):
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            username=username,
            date_of_birth=date_of_birth,
            password=password,
            is_superuser=True,
            **kwargs
        )
        
        

@login_required(login_url='signin')
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Check if the current user is the author of the post
    if post.user == request.user:
        post.delete()
        messages.success(request, "Post deleted successfully.")
    else:
        return HttpResponseForbidden("You are not allowed to delete this post.")
    
    # Redirect back to the user's profile after deletion
    return redirect('profile', user_id=request.user.id)

