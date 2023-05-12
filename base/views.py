from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')
def description(request):
    return render(request, 'description.html')