from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(UserCreationForm):
	class Meta:
		model = User
		fields = ["email", "password"]

class LoginForm(AuthenticationForm):
	class Meta:
		model = User
		fields = ["email", "password"]
