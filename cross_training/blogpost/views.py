from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return HttpResponse("Main Page, will soon contain register and login buttons")
