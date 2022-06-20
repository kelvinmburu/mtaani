from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm, BusinessForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import NeighbourHood, Profile, Business, Post
from .forms import UpdateProfileForm, NeighbourhoodForm, PostForm
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from .emails import send_welcome_email

# Create your views here.

def index(request):
    page = 'login'
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User doesnt exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are successfuly logged in")
            return redirect('home')
        else:
            messages.error(request, 'Username or password doesnt exist')
    context = {'page': page}
    return render(request, 'mtaaniapp/auth.html', context)

def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            recipient = User(username=username, email=email)
            send_welcome_email(username, email)

            profile = Profile.objects.create(user=user)
            profile.save()
            
            page = 'register'
            return render(request, 'mtaaniapp/success.html', {'page': page})
    context = {'form': form}
    return render(request, 'mtaaniapp/auth.html', context)

def home(request):
    context = {}
    return render(request, 'mtaaniapp/index.html', context)
    
def contact(request):
    return render(request, 'mtaaniapp/contact.html')

def support(request):
    return render(request, 'mtaaniapp/support.html')

def logout_user(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def hoods(request):
    all_hoods = NeighbourHood.objects.all()
    all_hoods = all_hoods[::-1]
    params = {'all_hoods': all_hoods}
    return render(request, 'mtaaniapp/all_hoods.html', params)

@login_required(login_url='login')
def create_hood(request):
    context = {}
    return render(request, 'mtaaniapp/newhood.html', context)
    
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
            return redirect('single-hood', hood.id)
    else:
        form = BusinessForm
        params = {
            'hood':hood,
            'business': business,
            'form': form,
            'posts': posts
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
        return redirect('single-hood', hood.id)
    else:
        form = PostForm()
    return render(request, 'mtaaniapp/post.html', {'form': form})

@login_required(login_url='login')
def join_hood(request, id):
    neighbourhood = get_object_or_404(NeighbourHood, id=id)
    request.user.profile.neighbourhood = neighbourhood
    request.user.profile.save()
    return redirect('hood')

@login_required(login_url='login')
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