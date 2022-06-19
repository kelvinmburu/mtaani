from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm, BusinessForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import NeighbourHood, Profile, Business, Post
from .forms import UpdateProfileForm, NeighbourhoodForm, PostForm
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    context = {}
    return render(request, 'mtaaniapp/index.html', context)


def index(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are successfuly logged in")
            return redirect('index')
    return render(request, 'mtaaniapp/login.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data('username')
            password = form.cleaned_data('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'mtaaniapp/signup.html', {'form': form})