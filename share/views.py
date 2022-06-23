from django.shortcuts import render
from .models import Image, Profile, Comment
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import UploadForm, ProfileForm, CommentForm, RegisterForm
from django.urls.base import reverse
from django.http.response import Http404


# Create your views here.
def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = RegisterForm()
    return render(request, 'registration/signup.html', {'form': form})


def index(request):
    images = Image.images()
    users = User.objects.exclude(id=request.user.id)
    context = {
        "users": users,
        "images": images[::1]
    }
    return render(request, 'index.html', context)


def profile(request, username):
    current_user = request.user
    user = User.objects.get(username=current_user.username)
    user_select = User.objects.get(username=username)
    if user_select == user:
        return redirect('profile', username=request.user.username)

    posts = Image.objects.filter(user=user_select.id)

    ctx = {
        "posts": posts,
        "profile": profile,
        'user': user,
    }
    return render(request, 'main/profile.html', ctx)


def post(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user.profile
            post.save()
            return redirect('landing')
    else:
        form = UploadForm()
    return render(request, 'post_image.html', {"form": form})


def comment(request, id):
    image = get_object_or_404(Image, pk=id)
    comments = image.comment.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.photo = image
            comment.user = request.user.profile
            comment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = CommentForm()
    context = {
        'image': image,
        'form': form,
        'comments': comments,
    }
    return render(request, 'post.html', context)


def like_video(request, id):
    post = Image.objects.get(pk=id)
    is_liked = False
    user = request.user.profile
    try:
        profile = Profile.objects.get(user=user.user)
        print(profile)

    except Profile.DoesNotExist:
        raise Http404()
    if post.likes.filter(id=user.user.id).exists():
        post.likes.remove(user.user)
        is_liked = False
    else:
        post.likes.add(user.user)
        is_liked = True
    return HttpResponseRedirect(reverse('landing'))


def profile(request, username):
    images = request.user.profile.images.all()
    if request.method == 'POST':
        prof_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if prof_form.is_valid():
            prof_form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        prof_form = ProfileForm(instance=request.user.profile)
    context = {
        'prof_form': prof_form,
        'images': images,
    }
    return render(request, 'profile.html', context)


def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('profile')
    else:
        form = ProfileForm()
    return render(request, 'edit_profile.html', {"form": form})


def search_profile(request):
    if 'search_user' in request.GET and request.GET['search_user']:
        name = request.GET.get("search_user")
        results = Profile.search_profile(name)
        print(results)
        message = name
        params = {
            'results': results,
            'message': message
        }
        return render(request, 'results.html', params)
    else:
        message = "You did not make a selection"
    return render(request, 'results.html', {'message': message})


def user_profile(request, username):
    user_prof = get_object_or_404(User, username=username)
    if request.user == user_prof:
        return redirect('profile', username=request.user.username)
    user_posts = user_prof.profile.images.all()


    context = {
        'user_prof': user_prof,
        'user_posts': user_posts,

    }
    return render(request, 'user_profile.html', context)







