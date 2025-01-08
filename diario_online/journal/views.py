from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Person, Journal

def home(request):
    if request.method == 'GET':
        return render(request, 'home.html')
    
def write(request):
    people = Person.objects.all()
    if request.method == 'GET':
        return render(request, 'write.html', {'people': people})
    
    if request.method == 'POST':
        tittle = request.POST.get('titulo')
        tags = request.POST.getlist('tags')
        person = request.POST.getlist('pessoas')
        text = request.POST.get('texto')

        print(tittle, tags, person, text)

        return redirect(write)
    
def person_registration(request):
    if request.method == 'GET':
        return render(request, 'person_registration.html')
    
    if request.method == 'POST':
        name = request.POST.get('nome')
        foto = request.FILES.get('foto')

        try:
            person = Person(
                name=name,
                foto=foto
            )
        except:
            return redirect(person_registration)

        person.save()

        return redirect('write')