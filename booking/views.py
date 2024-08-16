from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from .forms import *
from .models import *

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, _("You've been logged in successfully"))
                return HttpResponseRedirect(reverse("index"))
            else:
                messages.error(request, _("Invalid username and/or password"))
                return render(request, "login.html", {'form': form})
        else:
            messages.error(request, _("This username is not valid. Username should contain alphanumeric characters only."))
            return render(request, "login.html", {'form': form})
    else:
        form = LoginForm()
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                account = form.save(commit=False)
                account.set_password(form.cleaned_data["password"])
                account.save()
            except:
                messages.error(request, _("Username already exists"))
                return render(request, "register.html", {'form': form})
            account = authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            login(request, account)
            return redirect('index')
        else:
            messages.error(request, _("Information is not valid. Please check information again."))
            return render(request, "register.html", {'form': form})
    else:
        form = SignUpForm()
        return render(request, "register.html", {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def index(request):
    return render(request, 'homepage.html')
