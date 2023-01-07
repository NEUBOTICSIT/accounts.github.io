from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

from Accounting_Software_App.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model=User
        fields= ('email',)
        
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields=('email',)


