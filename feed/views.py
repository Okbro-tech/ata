from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Post
# Create your views here.


def redirecthome(request):
    return redirect('home')

@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    posts = Post.objects.all()
    print("posts:")
    print(posts)
    return render(request, 'socialmedia.html', {'user_profile': user_profile, 'posts': posts})

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password != password2:
            messages.info(request, 'Password not matching')
            return redirect('signup')
        
        if User.objects.filter(username=username).exists():
            messages.info(request, "Username taken")
            return redirect('signup')

        user = User.objects.create_user(username=username, password=password)
        user.save()
        
        #TO DO: log user in and redirect to settings page
        user_login=auth.authenticate(username=username,password=password)
        auth.login(request,user_login)


        user_model = User.objects.get(username=username)
        new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
        new_profile.save()
        return redirect('signin')

    else:
        return render(request, 'signup.html')
    
def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Credentials Invalid")
            return redirect('signin')
        
    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')    
def logout(request):
    return redirect('signin')

@login_required(login_url='signin')
def profile(request):
    return render(request, "profile.html")

@login_required(login_url='signin')
def upload(request):
    if request.method == "POST":
        user = request.user
        image = request.FILES.get('image_upload')  # Get the uploaded image
        caption = request.POST.get('caption', '')  # Get the caption (default to empty string if none provided)

        # Debugging: Print the uploaded data
        print(f"User: {user}, Image: {image}, Caption: {caption}")

        # Ensure image is provided before attempting to create the post
        if image:
            try:
                new_post = Post.objects.create(user=user, image=image, caption=caption)
                new_post.save()
                messages.success(request, "Post uploaded successfully!")
                print("Post successfully saved to the database.")
            except Exception as e:
                print(f"Error saving post: {e}")
                messages.error(request, "Failed to upload post.")
        else:
            print("Image not provided.")
            messages.error(request, "Image is required for uploading a post.")

        return redirect("/")
    else:
        return redirect("/")

