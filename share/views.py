from django.shortcuts import render
from .models import Image, Profile, Follow, Comment
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import UploadForm, ProfileForm, CommentForm, RegisterForm
from django.urls.base import reverse
from django.http.response import Http404


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

