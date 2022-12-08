from django.shortcuts import render, HttpResponse

def index(request):
    return render(request, 'index.html')

def signup(request):
    return render(request, 'signup.html')

def home(request):
    return HttpResponse('this is home')
