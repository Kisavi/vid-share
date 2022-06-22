from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import CommentForm 
from django.urls.base import reverse
from django.http.response import Http404

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


def like_post(request, id):
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

def unfollow(request, to_unfollow):
    if request.method == 'GET':
        user_two_profile = Profile.objects.get(pk=to_unfollow)
        unfollow_d = Follow.objects.filter(follower=request.user.profile, followed=user_two_profile)
        unfollow_d.delete()
        return redirect('user_profile', user_two_profile.user.username)


# @login_required(login_url='login')
def follow(request, to_follow):
    if request.method == 'GET':
        user_three_profile = Profile.objects.get(pk=to_follow)
        follow_s = Follow(follower=request.user.profile, followed=user_three_profile)
        follow_s.save()
        return redirect('user_profile', user_three_profile.user.username)