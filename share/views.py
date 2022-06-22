from django.shortcuts import render
from .models import Profile
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import ProfileForm
from django.http.response import Http404


def profile(request, username):
    current_user = request.user
    user = User.objects.get(username=current_user.username)
    user_select = User.objects.get(username=username)
    if user_select == user:
        return redirect('profile', username=request.user.username)


    ctx = {
        
        "profile": profile,
        'user': user,
    }
    return render(request, 'main/profile.html', ctx)
def profile(request, username):
    current_user = request.user
    user = User.objects.get(username=current_user.username)
    user_select = User.objects.get(username=username)
    if user_select == user:
        return redirect('instagram:profile', username=request.user.username)

    posts = Image.objects.filter(user=user_select.id)

    ctx = {
        "posts": posts,
        "profile": profile,
        'user': user,
    }
    return render(request, 'main/profile.html', ctx)

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


