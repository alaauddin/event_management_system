from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from datetime import date
import xlwt
from django.http import HttpResponse
from operator import attrgetter
import csv

def change_event_status_to_published(pk):
    try:
        event = Event.objects.get(pk=pk)
        
        # Check if the event's date is today
        if event.date == date.today() or event.date < date.today() :
            if event.status != "canceled":
                event.status = "published"
                event.save()
                return "ok"
            else:
                return "Event is canceled"
        else:
            return "Event date is not today"

    except Event.DoesNotExist:
        return "Event not found"
    



def events_list(request):
    conference = Conference.objects.all()
    workshop = Workshop.objects.all()
    social_event = SocialEvent.objects.all()


    for i in conference:
        change_event_status_to_published(i.pk)

    for i in workshop:
        change_event_status_to_published(i.pk)

    for i in social_event:
        change_event_status_to_published(i.pk)

        
    # Handle form submission
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    status = request.GET.get('status')

    if date_from:
        conference = conference.filter(date__gte=date_from)
        workshop = workshop.filter(date__gte=date_from)
        social_event = social_event.filter(date__gte=date_from)

    if date_to:
        conference = conference.filter(date__lte=date_to)
        workshop = workshop.filter(date__lte=date_to)
        social_event = social_event.filter(date__lte=date_to)

    if status:
        conference = conference.filter(status=status)
        workshop = workshop.filter(status=status)
        social_event = social_event.filter(status=status)

    # Get status choices from the model
    status_choices = Conference.STATUS_CHOICES

    context = {
        'conference': conference,
        'workshop': workshop,
        'social_event': social_event,
        'date_from': date_from,
        'date_to': date_to,
        'status': status,
        'status_choices': status_choices,
    }

    return render(request, 'index.html', context)




def signup(request):
    form = SignUpForm()
    if request.method == "POST":
        
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request,user)
            return redirect('index')
          
    return render(request, 'signup.html', {'form':form})



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
            workshop.set_price()
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
    workshop = get_object_or_404(Workshop, pk=pk)
    workshop.delete()
    return redirect('events_list')



def create_social_event(request):
    if request.method == 'POST':
        form = SocialEventForm(request.POST)
        if form.is_valid():
            social_event = form.save(commit=False)
            social_event.create_by = request.user
            social_event.set_price()
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
    social_event = get_object_or_404(SocialEvent, pk=pk)
    social_event.delete()
    return redirect('events_list')


def draft_event(request):
    conferences = Conference.objects.filter(status="draft")
    workshops = Workshop.objects.filter(status="draft")
    social_events = SocialEvent.objects.filter(status="draft")

    # Combine all events into a single list
    all_events = list(conferences) + list(workshops) + list(social_events)

    # Sort events by date
    all_events_sorted = sorted(all_events, key=attrgetter('date'))

    context = {'events': all_events_sorted}
    return render(request, 'draft_events.html', context)


def completed_events(request):
    conferences = Conference.objects.filter(status="published")
    workshops = Workshop.objects.filter(status="published")
    social_events = SocialEvent.objects.filter(status="published")

    # Combine all completed events into a single list
    all_completed_events = list(conferences) + list(workshops) + list(social_events)

    context = {'events': all_completed_events}
    return render(request, 'completed_events.html', context)


def cancelled_events(request):
    conferences = Conference.objects.filter(status="canceled")
    workshops = Workshop.objects.filter(status="canceled")
    social_events = SocialEvent.objects.filter(status="canceled")

    # Combine all cancelled events into a single list
    all_cancelled_events = list(conferences) + list(workshops) + list(social_events)
    

    context = {'events': all_cancelled_events}
    return render(request, 'cancelled_events.html', context)


def location_list(request):
    locations = Location.objects.all()
    context = {'locations': locations}
    return render(request, 'location_list.html', context)

def create_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('location_list')  # Adjust the URL name based on your project
    else:
        form = LocationForm()

    return render(request, 'create_location.html', {'form': form})


def edit_location(request, location_id):
    location = get_object_or_404(Location, pk=location_id)

    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            return redirect('location_list')  # Adjust the URL name based on your project
    else:
        form = LocationForm(instance=location)

    return render(request, 'edit_location.html', {'form': form, 'location': location})



def delete_location (request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    location.delete()
    redirect('location_list')



def attendee_registration(request, event_id):
    # Assuming you have a function to get the event based on the event_id
    event = Event.objects.get(pk=event_id)

    if request.method == 'POST':
        form = AttendeeRegistrationForm(request.POST)
        if form.is_valid():
            # Create a new Attendee instance and link it to the specified event
            attendee = form.save(commit=False)
            attendee.save()
            # Assuming you have a related_name 'registrations' in your Event model
            registration = Registration.objects.create(
                participant=attendee,
                event = event,
            )

            # Redirect to a success page or do something else
            return redirect('draft_event')
    else:
        form = AttendeeRegistrationForm()

    return render(request, 'attendee_registration.html', {'form': form, 'event': event})




def volunteer_registration(request, event_id):
    # Assuming you have a function to get the event based on the event_id
    event = Event.objects.get(pk=event_id)

    if request.method == 'POST':
        form = VolunteerRegistrationForm(request.POST)
        if form.is_valid():
            # Create a new Volunteer instance and link it to the specified event
            volunteer = form.save(commit=False)
            volunteer.save()
            # Assuming you have a related_name 'registrations' in your Event model
            registration = Registration.objects.create(
                participant=volunteer,
                event = event,
            )

            # Redirect to a success page or do something else
            return redirect('draft_event')
    else:
        form = VolunteerRegistrationForm()

    return render(request, 'volunteer_registration.html', {'form': form, 'event': event})


def speaker_registration(request, event_id):
    # Assuming you have a function to get the event based on the event_id
    event = Event.objects.get(pk=event_id)

    if request.method == 'POST':
        form = SpeakerRegistrationForm(request.POST)
        if form.is_valid():
            # Create a new Speaker instance and link it to the specified event
            speaker = form.save(commit=False)
            speaker.save()
            # Assuming you have a related_name 'registrations' in your Event model
            registration = Registration.objects.create(
                participant=speaker,
                event = event,
            )

            # Redirect to a success page or do something else
            return redirect('draft_event')
    else:
        form = SpeakerRegistrationForm()

    return render(request, 'speaker_registration.html', {'form': form, 'event': event})


def organizer_registration(request, event_id):
    # Assuming you have a function to get the event based on the event_id
    event = Event.objects.get(pk=event_id)

    if request.method == 'POST':
        form = OrganizerRegistrationForm(request.POST)
        if form.is_valid():
            # Create a new Organizer instance and link it to the specified event
            organizer = form.save(commit=False)
            organizer.save()
            # Assuming you have a related_name 'registrations' in your Event model
            registration = Registration.objects.create(
                participant=organizer,
                event = event,
            )

            # Redirect to a success page or do something else
            return redirect('draft_event')
    else:
        form = OrganizerRegistrationForm()

    return render(request, 'organizer_registration.html', {'form': form, 'event': event})




def export_attendees(request, event_id):
    # Fetch the event
    event = get_object_or_404(Event, pk=event_id)

    # Set response headers for CSV file download
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={event.title}_attendees.csv'

    # Create a CSV writer object with comma delimiter (you can change it to tab if needed)
    writer = csv.writer(response, delimiter=',')

    # Write headers
    headers = ['Name', 'Email', 'Phone', 'Organization']
    writer.writerow(headers)

    # Write attendee data
    attendees = event.registrations.filter(participant__attendee__isnull=False).select_related('participant__attendee')

    for registration in attendees:
        attendee = registration.participant.attendee
        print(attendee.name, attendee.email, attendee.phone, attendee.organization)
        writer.writerow([attendee.name, attendee.email, attendee.phone, attendee.organization])

    return response

def export_volunteers(request, event_id):
    # Fetch the event
    event = get_object_or_404(Event, pk=event_id)

    # Set response headers for CSV file download
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={event.title}_volunteers.csv'

    # Create a CSV writer object
    writer = csv.writer(response)

    # Write headers
    headers = ['Name', 'Email', 'Phone', 'Tasks']
    writer.writerow(headers)

    # Write volunteer data
    volunteers = event.registrations.filter(participant__volunteer__isnull=False).select_related('participant__volunteer')
    for registration in volunteers:
        volunteer = registration.participant.volunteer
        writer.writerow([volunteer.name, volunteer.email, volunteer.phone, volunteer.tasks])

    return response


def export_organizers(request, event_id):
    # Fetch the event
    event = get_object_or_404(Event, pk=event_id)

    # Set response headers for CSV file download
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={event.title}_organizers.csv'

    # Create a CSV writer object
    writer = csv.writer(response)

    # Write headers
    headers = ['Name', 'Email', 'Position']
    writer.writerow(headers)

    # Write organizer data
    organizers = event.registrations.filter(participant__organizer__isnull=False).select_related('participant__organizer')
    for registration in organizers:
        organizer = registration.participant.organizer
        writer.writerow([organizer.name, organizer.email, organizer.position])

    return response


def export_speakers(request, event_id):
    # Fetch the event
    event = get_object_or_404(Event, pk=event_id)

    # Set response headers for CSV file download
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={event.title}_speakers.csv'

    # Create a CSV writer object
    writer = csv.writer(response)

    # Write headers
    headers = ['Name', 'Email', 'Expertise']
    writer.writerow(headers)

    # Write speaker data
    speakers = event.registrations.filter(participant__speaker__isnull=False).select_related('participant__speaker')
    for registration in speakers:
        speaker = registration.participant.speaker
        writer.writerow([speaker.name, speaker.email, speaker.expertise])

    return response


def cancel_event(request,event_id):
    event=get_object_or_404(Event, pk=event_id)
    event.status = "canceled"
    event.save()

    return redirect('draft_event')



def list_registered_attendees(request, event_id):
    # Retrieve the event using the event_id
    event = get_object_or_404(Event, pk=event_id)

    # Get the list of registered attendees for the event
    attendees = event.registrations.filter(participant__in=Attendee.objects.all())

    # Render the list of attendees in a template
    return render(
        request,
        'attendees_list.html',  # Replace with the actual template name
        {'event': event, 'attendees': attendees}
    )





def list_event_speakers(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    speakers = event.registrations.filter(participant__in=Speaker.objects.all())
    return render(
        request,
        'event_speakers_list.html',
        {'event': event, 'speakers': speakers}
    )


def list_event_organizers(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    organizers = event.registrations.filter(participant__in=Organizer.objects.all())
    return render(
        request,
        'event_organizers_list.html',
        {'event': event, 'organizers': organizers}
    )




def list_event_volunteers(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    volunteers = event.registrations.filter(participant__in=Volunteer.objects.all())
    return render(
        request,
        'event_volunteers_list.html',
        {'event': event, 'volunteers': volunteers}
    )