from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from .models import *
from .forms import ConferenceForm, WorkshopForm, SocialEventForm
from django.contrib.auth.decorators import login_required
# Create your views here.


def events_list(request):
    conference = Conference.objects.all()
    workshop = Workshop.objects.all()
    social_event = SocialEvent.objects.all()

    
    context = {
        'conference': conference,
        'workshop': workshop,
        'social_event': social_event,
    }


    return render(request, 'index.html', context)



@login_required
def create_conference(request):
    if request.method == 'POST':
        form = ConferenceForm(request.POST, request.FILES)
        if form.is_valid():
            conference = form.save(commit=False)  # Don't save to the database yet
            conference.create_by = request.user
            conference.set_price()
            conference = form.save()
            
            # Perform any additional logic or redirect to another page
            return redirect('events_list')
    else:
        form = ConferenceForm()

    return render(request, 'create_conference.html', {'form': form})


def edit_conference(request, pk):
    conference = get_object_or_404(Conference, pk=pk)

    if request.method == 'POST':
        form = ConferenceForm(request.POST, instance=conference)
        if form.is_valid():

            form.save()
            # Perform any additional logic or redirect to another page
            return redirect('events_list')
    else:
        form = ConferenceForm(instance=conference)

    return render(request, 'edit_conference.html', {'form': form})

def delete_conference(request, pk):
    conference = get_object_or_404(Conference, pk=pk)
    conference.delete()
    return redirect('events_list')



def create_workshop(request):
    if request.method == 'POST':
        form = WorkshopForm(request.POST)
        if form.is_valid():
            workshop = form.save(commit=False)  # Don't save to the database yet
            workshop.create_by = request.user
            workshop = form.save()
            # Perform any additional logic or redirect to another page
            return redirect('events_list')
    else:
        form = WorkshopForm()

    return render(request, 'create_workshop.html', {'form': form})



def edit_workshop(request, pk):
    workshop = get_object_or_404(Workshop, pk=pk)

    if request.method == 'POST':
        form = WorkshopForm(request.POST, instance=workshop)
        if form.is_valid():
            form.save()
            # Perform any additional logic or redirect to another page
            return redirect('events_list')
    else:
        form = WorkshopForm(instance=workshop)

    return render(request, 'edit_workshop.html', {'form': form})


def delete_workshop(request, pk):
    workshop = get_object_or_404(Conference, pk=pk)
    workshop.delete()
    return redirect('events_list')



def create_social_event(request):
    if request.method == 'POST':
        form = SocialEventForm(request.POST)
        if form.is_valid():
            social_event = form.save(commit=False)
            social_event.create_by = request.user
            social_event = form.save()
            # Perform any additional logic or redirect to another page
            return redirect('events_list')
    else:
        form = SocialEventForm()

    return render(request, 'create_social_event.html', {'form': form})

def edit_social_event(request, pk):
    social_event = get_object_or_404(SocialEvent, pk=pk)

    if request.method == 'POST':
        form = SocialEventForm(request.POST, instance=social_event)
        if form.is_valid():
            form.save()
            # Perform any additional logic or redirect to another page
            return redirect('events_list')
    else:
        form = SocialEventForm(instance=social_event)

    return render(request, 'edit_social_event.html', {'form': form})


def delete_social_event(request, pk):
    social_event = get_object_or_404(Conference, pk=pk)
    social_event.delete()
    return redirect('events_list')


