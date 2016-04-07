from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import User


# form used to register a user
class UserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ("name", "username", "email", "password1", "password2")

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "password",
        ]
