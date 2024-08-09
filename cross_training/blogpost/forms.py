from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
	email = forms.EmailInput()
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ["email", "password"]
		