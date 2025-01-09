from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Person, Journal
from django.contrib import messages
from datetime import datetime, timedelta

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
    
def day(request):
    if request.method == 'GET':
        if request.GET.get('date'):
            data = request.GET.get('date')
            formated_data = datetime.strptime(data, '%Y-%m-%d')
            journal_filtered = Journal.objects.filter(created_at__gte=formated_data).filter(created_at__lte=formated_data+timedelta(days=1))
            
            return render(request, 'day.html', {'journals':journal_filtered, 'total': journal_filtered.count(), 'date': data})
        
        return redirect('write')
    
def remove_day(request):
    if request.method == 'GET':
        data = request.GET.get('date')
        formated_data = datetime.strptime(data, '%Y-%m-%d')
        journal_filtered = Journal.objects.filter(created_at__gte=formated_data).filter(created_at__lte=formated_data+timedelta(days=1))

        journal_filtered.delete()

        return redirect('day')
