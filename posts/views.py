# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from urllib import quote_plus
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.generic import RedirectView

from posts.models import Post
from accounts.models import UserProfile


def post_list(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    queryset_list = Post.objects.all()
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
                Q(description__icontains=query)|
                Q(slug__icontains=query)|
                Q(user__username__icontains=query)
                ).distinct()
    paginator = Paginator(queryset_list, 8) # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    slug = request.GET.get("slug")
    if slug:
        obj = Post.objects.get(slug=slug)
        user = request.user
        if user in obj.likes.all():
            obj.likes.remove(user)
        else:
            obj.likes.add(user)
        obj.save()
    context = {
        "object_list": queryset,
        "page_request_var": page_request_var,
    }
    return render(request, "post_list.html", context)


def post_detail(request,slug=None):
    if not request.user.is_authenticated:
        return redirect("/login")

    instance = get_object_or_404(Post, slug=slug)
    share_string = quote_plus(instance.description)
    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id
    }

    context = {
        "instance": instance,
        "share_string": share_string,
    }
    return render(request, "post_detail.html", context)


class PostLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        print(slug)
        obj = get_object_or_404(Post, slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated():
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        print obj.likes.count()
        return url_


def post_create(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    if request.method=='POST':
        description = request.POST['description']
        try:
            photo = request.FILES['photo']
        except:
            messages.warning(request, "Not photo found!")
            return render(request, "post_form.html")
        print request.FILES['photo']
        print type(photo)
        post = Post.objects.create(user=request.user,
                                   description=description,
                                   photo=photo)
        post.save()
        messages.success(request, "Successfully posted!")
        return HttpResponseRedirect(post.get_absolute_url())
    return render(request, "post_form.html")


def user_profile_page(request, username):
    current_user = request.user
    if not current_user.is_authenticated:
        return redirect("/login")
    global user_profile, user
    try:
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
    except User.DoesNotExist:
        messages.warning(request, "User does not exist")
    except UserProfile.DoesNotExist:
        messages.warning(request, "User does not exist")

    posts = Post.objects.filter(user=user)
    context = {
        'posts': posts,
        'user_profile': user_profile,
        'current_user':current_user
    }
    return render(request, 'profile_detail.html', context)
