from django.shortcuts import render

def index(request):
	return HttpResponse("Main Page, will soon contain register and login buttons")
