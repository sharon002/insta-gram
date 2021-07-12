from django.shortcuts import render,redirect
from .models import Image, Profile,Comment
from django.contrib.auth.models import User
from .forms import CommentForm, ImageForm, ProfileUpdateForm, UserUpdateForm, PostIMageForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from .emails import send_welcome_email


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')


            return redirect('/accounts/login/')
            
    else:
        form = UserRegisterForm()
    return render(request, 'registration/registration_form.html', {'form':form})


def home(request):
    return render(request, 'images.html')


@login_required(login_url='/accounts/login/')
def all_images(request):
    all_users = User.objects.all()
    all_images = Image.objects.all()
    next = request.GET.get('next')
    if next: return redirect(next)
    return render(request, 'images.html',  {"all_images": all_images, "all_users":all_users})


def profile(request, username):
    profile = User.objects.get(username=username)
    try:
        profile_details = Profile.get_by_id(profile.id)
    except:
        profile_details = Profile.filter_by_id(profile.id)
    user_images = Image.get_profile_images(profile.id)

    return render(request, 'profiles/profile.html', {'profile':profile, 'profile_details':profile_details, 'user_images':user_images})


@login_required(login_url='/accounts/login')
def single_image(request, image_id):
    image = Image.get_image_id(image_id)
    comments = Comment.get_comments_by_images(image_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.image = image
            comment.user = request.user
            comment.save()
            return redirect('single_image', image_id=image_id)
    else:
        form = CommentForm()
        
    return render(request, 'single_image.html', {'image':image, 'form':form, 'comments':comments})


# @login_required(login_url='/accounts/login')
# def edit_profile(request):
#     if request.method == 'POST':
#         form = ProfileUpdateForm(request.POST, request.FILES)
#         if form.is_valid():
#             edit = form.save(commit=False)
#             edit.user = request.user
#             edit.save()
#             return redirect('edit_profile')
#     else:
#         form = ProfileUpdateForm()

#     return render(request, 'profiles/edit_profile.html', {'form':form})


# @login_required(login_url='/accounts/login')


def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('all_images')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form':u_form,
        'p_form':p_form
    }
    
    return render(request, 'profiles/profile_update.html', {'u_form':u_form, "p_form": p_form})


@login_required(login_url='/login')
def post_image(request):
    current_user = request.user
    if request.method == 'POST':
        form = PostIMageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.profile = current_user
            image.save()
        return redirect('all_images')
    else:
        form = PostIMageForm(auto_id=False)
    return render(request, 'upload_image.html', {"form": form})

def search(request):
    if 'search' in request.GET and request.GET['search']:
        search_term = request.GET.get('search')
        profiles = Profile.search_profile(search_term)
        message = f'{search_term}'

        return render(request, 'search.html',{'message':message, 'profiles':profiles})
    else:
        message = 'an empty search term!'
        return render(request, 'search.html', {'message':message})