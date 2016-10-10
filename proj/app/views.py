from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as _login, logout as _logout


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                _login(request, user)
                return redirect(reverse("index"))
    return render(request, "login.html")


def logout(request):
    _logout(request)
    return redirect(reverse("login"))


@login_required(login_url=reverse_lazy("login"))
def index(request):
    return render(request, "index.html")
