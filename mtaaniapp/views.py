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

def contact(request):
    return render(request, 'mtaaniapp/contact.html')

def support(request):
    return render(request, 'mtaaniapp/support.html')

def logout_user(request):
    logout(request)
    return redirect('home')

def hoods(request):
    all_hoods = NeighbourHood.objects.all()
    all_hoods = all_hoods[::-1]
    params = {'all_hoods': all_hoods}
    return render(request, 'mtaaniapp/all_hoods.html', params)

def create_hood(request):
    if request.method == 'POST':
        form = NeighbourhoodForm(request.POST, request.FILES)
        if form.is_valid():
            hood = form.save(commit=False)
            hood.admin = request.user.profile
            hood.save()
            return redirect('hood')
        else:
            form = NeighbourhoodForm()
        return render(request, 'mtaaniapp/newhood.html', {'form': form})
    
def single_hood(request, hood_id):
    hood = NeighbourHood.objects.get(id=hood_id)
    business = Business.objects.filter(neighbourhood=hood)
    posts = Post.objects.filter(hood=hood)
    posts = posts[::-1]
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            b_form = form.save(commit=False)
            b_form.neighbourhood = hood
            b_form.user = request.user.profile
            b_form.save()
            return redirect('single_hood', hood.id)
    else:
        form = BusinessForm
        params = {
            'hood':hood,
            'business': business,
            'form': form,
            'post': posts
        }
        return render(request, 'mtaaniapp/single_hood.html', params)
    
def hood_members(request, hood_id):
    hood = NeighbourHood.objects.get(id=hood_id)
    members = Profile.objects.filter(neighbourhood= hood)
    return render(request, 'mtaaniapp/members.html', {'members': members})

def create_post(request, hood_id):
    hood = NeighbourHood.objects.get(id=hood_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        post = form.save(commit=False)
        post.hood = hood
        post.user = request.user.profile
        return redirect('single_hood', hood.id)
    else:
        form = PostForm()
    return render(request, 'mtaaniapp/post.html', {'form': form})

def join_hood(request, id):
    neighbourhood = get_object_or_404(NeighbourHood, id=id)
    request.user.profile.neighbourhood = neighbourhood
    request.user.profile.save()
    return redirect('hood')

def leave_hood(request, id):
    hood = get_object_or_404(NeighbourHood, id=id)
    request.user.profile.neighbourhood = None
    request.user.profile.save()
    return redirect('hood')

def profile(request, username):
    return render(request, 'mtaaniapp/profile.html')

def edit_profile(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile', user.username)
    else:
        form = UpdateProfileForm(instance=request.user.profile)
    return render(request, 'mtaaniapp/editprofile.html', {'form': form})

def search_business(request):
    if request.method == 'POST':
        name = request.GET.get('title')
        results = Business.objects.filter(name__icontains=name).all()
        print(results)
        message = f'name'
        params = {
            'results': results,
            'message': message
        }
        return render(request, 'mtaaniapp/results.html', params)
    else:
        message = 'You have not searched for any category'
    return render(request, 'mtaaniapp/results.html')