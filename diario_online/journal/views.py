from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Person, Journal
from django.contrib import messages

def home(request):
    journals = Journal.objects.all().order_by('created_at')[:3]
    if request.method == 'GET':
        return render(request, 'home.html', {'journals':journals})
    
def write(request):
    people = Person.objects.all()
    if request.method == 'GET':
        return render(request, 'write.html', {'people': people})
    
    if request.method == 'POST':
        tittle = request.POST.get('titulo')
        tags = request.POST.getlist('tags')
        people = request.POST.getlist('pessoas')
        text = request.POST.get('texto')

        if len(tittle.strip()) == 0 or len(text.strip()) == 0:
            messages.add_message(request, messages.ERROR, "Os campos título ou texto não podem estar em branco!")
            return redirect('write')

        journal = Journal(
            tittle=tittle,
            text=text,
        )
        journal.set_tags(tags)
        journal.save()

        for id in people:
            person = Person.objects.get(id=id)
            journal.person.add(person)

        journal.save()  

        messages.add_message(request, messages.SUCCESS, "Diário salvo com sucesso!")
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