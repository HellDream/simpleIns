# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from PIL import Image
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from accounts.models import UserProfile
from .forms import UserLoginForm, UserRegisterForm, UserEditForm


# Create your views here.


def register(request):
    form = UserRegisterForm(request.POST or None, request.FILES or None)
    title = "Register"
    next = request.GET.get('next')
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        image = form.files.get('image')
        email = form.cleaned_data.get('email')
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        user_profile = UserProfile.objects.create(user=user)
        user_profile.image = image
        user_profile.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect("/")
    context = {
        "form": form,
        "title": title
    }
    return render(request, "form.html", context)


def login_view(request):
    form = UserLoginForm(request.POST or None)
    title = "Login"
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user=user)
        return redirect('/')
    context = {
        'form': form,
        'title': title
    }
    return render(request, "form.html", context)


def logout_view(request):
    print request.user.username
    logout(request)
    return redirect("/")


def profile_edit_view(request):
    form = UserEditForm(request.POST or None, request.FILES or None)
    title = "Edit-Profile"
    if not request.user.is_authenticated:
        return redirect("/")
    user_profile = UserProfile.objects.get(user=request.user)
    initial_data = {
        'signature': user_profile.signature,
        'image': user_profile.image
    }
    if form.is_valid():
        signature = form.cleaned_data.get("signature")
        if signature:
            user_profile.signature = signature
        image = form.files.get("image")
        if image:
            user_profile.image = image
        user_profile.save()
        return redirect("/user/" + user_profile.user.username)

    form = UserEditForm(initial=initial_data)
    context = {
        'form': form,
        'title': title
    }
    return render(request, 'form.html', context)
