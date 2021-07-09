from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .forms import ImageForm, ProfileForm, CommentsForm
from .models import Image, Profile, Comments, Likes
from friendship.models import Friend, Follow, Block

# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
    '''
    Function that returns website application home page.
    '''
    images = Image.get_images().order_by('-posted_on')
    profiles = User.objects.all()
    people = Follow.objects.following(request.user)
    comments = Comments.objects.all()
    likes = Likes.objects.all()

    return render(request, 'index.html', {'images': images, 'profiles': profiles, 'comments': comments, 'people':people, 'likes': likes})


@login_required(login_url='/accounts/login/')
def new_post(request):
    """
    Function that enables one to upload images
    """
    profile = Profile.objects.all()
    for profile in profile:

        if request.method == 'POST':
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.save(commit=False)
                image.profile = profile
                image.user = request.user
                image.save()
            return redirect('home')
        else:
            form = ImageForm()
    return render(request, 'new_post.html', {"form": form})


@login_required(login_url='/accounts/login/')
def like_post(request):
    image = get_object_or_404(Image, id=request.POST.get('image_id'))
    image.likes.add(request.user)
    return redirect('home')


@login_required(login_url='/accounts/login/')
def profile(request, user_id):
    """
    Function that enables one to see their profile
    """
    title = "Profile"
    images = Image.get_image_by_id(id=user_id).order_by('-posted_on')
    comments = Comments.objects.all()
    profiles = User.objects.get(id=user_id)
    users = User.objects.get(id=user_id)
    follow = len(Follow.objects.followers(users))
    following = len(Follow.objects.following(users))
    people = Follow.objects.following(request.user)
    return render(request, 'profile/profile.html', {'title': title, "images": images, "profiles": profiles, 'following':following, 'follow':follow, "comments": comments})


@login_required(login_url='/accounts/login/')
def edit_profile(request):
    """
    Function that enables one to edit their profile information
    """
    current_user = request.user
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
        return redirect('home')
    else:
        form = ProfileForm()
    return render(request, 'profile/edit-profile.html', {"form": form, })


@login_required(login_url='/accounts/login/')
def follow(request, user_id):
    other_user = User.objects.get(id=user_id)
    follow = Follow.objects.add_follower(request.user, other_user)

    return redirect('home')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            return HttpResponse('Click here to login.' '<a href="/accounts/login/"> click here </a>')
    else:
        form = SignupForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required(login_url='/accounts/login/')
def unfollow(request, user_id):
    other_user = User.objects.get(id=user_id)
    follow = Follow.objects.remove_follower(request.user, other_user)

    return redirect('home')


@login_required(login_url='/accounts/login/')
def search_user(request):
    """
    Function that searches for profiles based on the usernames
    """
    if 'username' in request.GET and request.GET["username"]:
        name = request.GET.get("username")
        searched_profiles = User.objects.filter(username__icontains=name)
        message = f"{name}"
        profiles = User.objects.all()
        # people = Follow.objects.following(request.user)
        print(profiles)
        return render(request, 'search.html', {"message": message, "usernames": searched_profiles, "profiles": profiles, })

    else:
        message = "Enter search term"
        return render(request, 'search.html', {"message": message})


@login_required(login_url='/accounts/login/')
def add_comment(request, image_id):
    images = get_object_or_404(Image, pk=image_id)
    if request.method == 'POST':
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.image = images
            comment.save()
    return redirect('home')


def like(request, image_id):
    pass
    current_user = request.user
    liked_post = Image.objects.get(id=image_id)
    new_like, created = Likes.objects.get_or_create(
        user_like=current_user, liked_post=liked_post)
    new_like.save()

    return redirect('home')