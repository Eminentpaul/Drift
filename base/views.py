from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, get_list_or_404

# Create your views here.

def home(request):
    return render(request, 'base/index.html')


def about(request):
    return render(request, 'base/about.html')


def how_it_works(request):
    return render(request, 'base/how-it-works.html')

def news(request):
    return render(request, 'base/blog.html')


def news_detail(request):
    return render(request, 'base/blog-details.html')


def contact(request):
    return render(request, 'base/contact.html')