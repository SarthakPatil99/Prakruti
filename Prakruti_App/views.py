from django.shortcuts import render, HttpResponse

jinja = {}

def index(request):
    return render(request, 'index.html')

def signup(request):
    return render(request, 'signup.html')


def home(request):
    return HttpResponse('this is home')


def analyze(request):
    return render(request, 'user/Analyzer.html')


def recommend(request):
    return render(request, 'user/Reccomender.html')


def shopping(request):
    return render(request, 'user/Shopping.html')