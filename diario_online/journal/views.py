from django.shortcuts import render, redirect
from django.http import HttpResponse

def home(request):
    if request.method == 'GET':
        return render(request, 'home.html')
    
def write(request):
    if request.method == 'GET':
        return render(request, 'write.html')
    
    if request.method == 'POST':
        tittle = request.POST.get('titulo')
        tags = request.POST.getlist('tags')
        person = request.POST.getlist('pessoas')
        text = request.POST.get('texto')

        print(tittle, tags, person, text)

        return redirect(write)