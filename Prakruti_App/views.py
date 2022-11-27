from django.shortcuts import render, HttpResponse

def index(request):
    return render(request, 'index.html')

def about(request):
    return HttpResponse('this is about')

def home(request):
    return HttpResponse('this is home')
