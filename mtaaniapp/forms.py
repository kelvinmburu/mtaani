from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, NeighbourHood, Business, Post
from pyuploadcare.dj.forms import ImageField

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='Required. Inform a valid')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'neighbourhood')
        
class NeighbourhoodForm(forms.ModelForm):
    class Meta:
        model = Business
        exclude = ('admin')