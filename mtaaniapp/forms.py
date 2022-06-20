from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile, NeighbourHood, Business, Post

class SignupForm(UserCreationForm):
    
    email = forms.EmailField(max_length=200, label='',widget=forms.EmailInput(attrs={'class': 'form-control mb-4', 'placeholder': 'Email'}))
    username =forms.CharField(max_length=200, label='',widget=forms.TextInput(attrs={'class': 'form-control mb-4','placeholder': 'Username'}))
    password1 = forms.CharField(max_length=200,label='',widget=forms.PasswordInput(attrs={'class': 'form-control mb-4', 'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=200, label='',widget=forms.PasswordInput(attrs={'class': 'form-control mb-4','placeholder': 'Confirm password'}))
    
    
    class Meta():
        model = User
        fields = ('email', 'username', 'password1', 'password2')
        
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'neighbourhood')
        
class NeighbourhoodForm(forms.ModelForm):
    class Meta:
        model = NeighbourHood
        exclude = ('admin',)
        
class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        exclude = ('user', 'neighbourhood')
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('user', 'hood')
    