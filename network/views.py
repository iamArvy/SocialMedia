from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from .models import User, Post, Comment


def index(request, type):
    user = request.user
    if type == 'all':
        all_posts = Post.objects.order_by('-created_at')

    if type == 'following':
        if user.is_authenticated:
            idols = user.following.all()
            content = []
            for idol in idols:
                idol_posts = idol.posts.all()
                content.extend(idol_posts)
            all_posts = sorted(content, key=lambda x: x.created_at, reverse=True)
        else:
            return redirect('login')
    for each in all_posts:
        if user in each.likes.all():
            each.liked = True
        else:
            each.liked = False

        if user == each.user:
            each.is_owner = True
    paginator = Paginator(all_posts, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "network/index.html", {'posts': posts})

@login_required
def profile(request, name):
    # user = request.user
    content = get_object_or_404(User, username=name)
    all_posts = content.posts.all().order_by('-created_at')
    user = request.user
    is_follow = content.followers.filter(id=user.id).exists()
    paginator = Paginator(all_posts, 10)
    page = request.GET.get('page')
    for each in all_posts:
        if user in each.likes.all():
            each.liked = True
        else:
            each.liked = False
            
        if user == each.user:
            each.is_owner = True
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "network/profile.html", {'content' : content, 'posts' : posts, 'is_follow' : is_follow})

@login_required
@csrf_exempt
@require_POST
def like(request, id, type):
    user = request.user
    if type == 'post':
        content = get_object_or_404(Post, id=id)
    if type == 'comment':
        content = get_object_or_404(Comment, id=id)

    if content.likes.filter(id=user.id).exists():
        content.likes.remove(user)
        liked = False
    else:
        content.likes.add(user)
        liked = True
    like_count = content.likes.count()
    return JsonResponse({'liked': liked, 'like_count': like_count})

@login_required
@csrf_exempt
@require_POST
def follow(request, name, type):
    user = request.user
    content = get_object_or_404(User, username=name)
    if type == 'follow':
        user.following.add(content)
        content.followers.add(user)
        follow = True
    if type == 'unfollow':
        user.following.remove(content)
        content.followers.remove(user)
        follow = False
    user.save()
    content.save()
    return JsonResponse({'success': True, 'follow' : follow})


@login_required
def unfollow(request, name):
    user = request.user
    content = get_object_or_404(User, username=name)
    user.following.remove(content)
    content.followers.remove(user)
    user.save()
    content.save()
    return JsonResponse({'success': True})
    # messages.success(request, _("You are now following %s")% (content))

@csrf_exempt
@login_required
@require_POST
def create(request, type):
    data = json.loads(request.body)
    content = data.get('content')
    user = request.user
    if content:
        if type == "post":
            post = Post.objects.create(user=request.user, post=content)
            post.save()
            user.posts.add(post)
            user.save
        if type == "comment":
            comment = Comment.objects.create(user=user, comment=content)
            comment.save()
            id = data.get('post_id')
            post = Post.objects.get(id=id)
            post.comments.add(comment)
            post.save

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Post text cannot be empty'})

@csrf_exempt
@login_required
@require_POST
def edit(request, id, type):
    data = json.loads(request.body)
    content = data.get('content')
    user = request.user
    if content:
        if type == 'post':
            post = Post.objects.get(id=id)
            if user == post.user:
                post.post = content
                post.save()
                return JsonResponse({'success': True})
            else: 
                return JsonResponse({'success': False, 'error': 'UNAUTHORIZED USER'})
            
        if type == 'comment':
            comment = Comment.objects.get(id=id)
            if user == comment.user:
                comment.comment = content
                comment.save()
                return JsonResponse({'success': True})
            else: 
                return JsonResponse({'success': False, 'error': 'UNAUTHORIZED USER'})
        
    else:
        return JsonResponse({'success': False, 'error': 'Post text cannot be empty'})
    
@csrf_exempt
@login_required
@require_POST
def delete(request, id, type):
    user = request.user
    if type == 'post':
        post = Post.objects.get(id=id)
        if user == post.user:
            post.delete()
            return JsonResponse({'success': True})
        else: 
            return JsonResponse({'success': False, 'error': 'UNAUTHORIZED USER'})
    if type == 'comment':
        comment = Post.objects.get(id=id)
        if user == comment.user:
            comment.delete()
            return JsonResponse({'success': True})
        else: 
            return JsonResponse({'success': False, 'error': 'UNAUTHORIZED USER'})
    
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
