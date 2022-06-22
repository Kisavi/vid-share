from django.shortcuts import render
from .models import Profile
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import ProfileForm


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

    followers = Follow.objects.filter(followed=user_prof.profile)
    follow_status = None
    for follower in followers:
        if request.user.profile == follower.follower:
            follow_status = True
        else:
            follow_status = False
    context = {
        'user_prof': user_prof,
        'user_posts': user_posts,
        'followers': followers,
        'follow_status': follow_status
    }
    return render(request, 'user_profile.html', context)



