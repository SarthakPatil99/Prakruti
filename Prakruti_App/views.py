from django.shortcuts import render, HttpResponse


def index(request):
    return render(request, 'index.html')


def about(request):
    return HttpResponse('this is about')


def home(request):
    return HttpResponse('this is home')


def analyze(request):
    return render(request, 'user/Analyzer.html')


def recommend(request):
    return render(request, 'user/Reccomender.html')


def shopping(request):
    return render(request, 'user/Shopping.html')