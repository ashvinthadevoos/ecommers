from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from store.models import Reviews

class RegistrationForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model=User
        fields=['first_name','last_name','username','email']
        widgets={
            'first_name':forms.TextInput(attrs={'class':"form-control"}),
            'last_name':forms.TextInput(attrs={'class':"form-control"}),
            'username':forms.TextInput(attrs={'class':"form-control"}),
            'email':forms.EmailInput(attrs={'class':"form-control"}),
        }

class LoginForm(forms.Form):
    username=forms.CharField(max_length=200)
    password=forms.CharField(max_length=200)

class ReviewForm(forms.ModelForm):
    class Meta:
        model=Reviews
        fields=['comment','rating']