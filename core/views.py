from django.shortcuts import get_object_or_404
from .models import Post, Profile, Comment
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Post

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def login_page(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('/dashboard/')

    return render(request, 'login.html')

def signup_page(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return redirect('/signup/')

        user = User.objects.create_user(
            username=username,
            password=password
        )

        Profile.objects.create(
            user=user
        )

        return redirect('/login/')

    return render(request, 'signup.html')

def dashboard(request):

    posts = Post.objects.all().order_by('-id')

    profile = request.user.profile

    if request.method == "POST":

        image = request.FILES.get('image')

        if image:

            profile.image = image
            profile.save()

            return redirect('/dashboard/')

        bio = request.POST.get('bio')

        if bio is not None:

            profile.bio = bio
            profile.save()

            return redirect('/dashboard/')

    return render(request, 'dashboard.html', {
        'posts': posts
    })

def post_page(request):

    if request.method == "POST":

        content = request.POST.get('content')

        Post.objects.create(
            user=request.user,
            content=content
        )

        return redirect('/dashboard/')

    return render(request, 'post.html')

def logout_page(request):

    logout(request)

    return redirect('/login/')

def logout_page(request):

    logout(request)

    return redirect('/login/')

def delete_post(request, id):

    post = get_object_or_404(Post, id=id)

    if post.user == request.user:
        post.delete()

    return redirect('/dashboard/')

def edit_post(request, id):

    post = get_object_or_404(Post, id=id)

    if post.user != request.user:
        return redirect('/dashboard/')

    if request.method == "POST":

        post.content = request.POST.get('content')
        post.save()

        return redirect('/dashboard/')

    return render(request, 'edit.html', {
        'post': post
    })

def like_post(request, id):

    post = get_object_or_404(Post, id=id)

    if request.user in post.likes.all():

        post.likes.remove(request.user)

    else:

        post.likes.add(request.user)

    return redirect('/dashboard/')

def add_comment(request, id):

    post = get_object_or_404(Post, id=id)

    if request.method == "POST":

        text = request.POST.get('text')

        Comment.objects.create(
            post=post,
            user=request.user,
            text=text
        )

    return redirect('/dashboard/')

def profile_page(request, username):

    user = User.objects.get(username=username)

    posts = Post.objects.filter(user=user)

    return render(request, 'profile.html', {
        'profile_user': user,
        'posts': posts
    })

def follow_user(request, username):

    profile_user = User.objects.get(username=username)

    profile = profile_user.profile

    if request.user in profile.followers.all():

        profile.followers.remove(request.user)

    else:

        profile.followers.add(request.user)

    return redirect(f'/profile/{username}/')