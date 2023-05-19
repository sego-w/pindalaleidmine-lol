from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.

def home(request):
    return render(request, 'home.html')
def description(request):
    return render(request, 'description.html')

def paint(request):
    if request.method == 'GET':
        return render(request, 'paint.html')
    elif request.method == 'POST':
        filename = request.POST['save_fname']
        data = request.POST['save_cdata']
        image = request.POST['save_image']
        file_data = Files(name=filename, image=data, canvas_image=image)
        file_data.save()
        return HttpResponseRedirect('/')