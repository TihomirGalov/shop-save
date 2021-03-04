from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import RegisterForm
from django.shortcuts import redirect
import os
from django.conf import settings


def register(response):
    if response.method == 'POST':
        form = RegisterForm(response.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = True
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(response, user)
            return redirect('/')

    else:
        form = RegisterForm()
    return render(response, os.path.join(settings.BASE_DIR, "shopassist/templates/admin/register.html"), {'form': form})