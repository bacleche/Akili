from django.shortcuts import render,redirect

# Create your views here.


def home_index(request):
    return render(request, 'index.html')