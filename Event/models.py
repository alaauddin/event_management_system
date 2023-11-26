


from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name





# Base Event class
class Event(models.Model):
    tenant = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    date = models.DateField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='events')
    description = models.TextField(max_length=1000)
    create_by = models.ForeignKey(User, related_name='events',on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('canceled', 'Canceled'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    discout = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def set_price(self):
        self.price = self.location.price - self.discout
        return self.price

    def display_event_details(self):
        return f"Event: {self.title}, Date: {self.date}"

    def get_event_type(self):
        return "Event"

    def __str__(self):
        return self.title


class Conference(Event):
    theme = models.CharField(max_length=100)

    def display_event_details(self):
        return f"Conference: {self.title}, Theme: {self.theme}, Date: {self.date}"

    def get_event_type(self):
        return "Conference"

class Workshop(Event):
    topic = models.CharField(max_length=100)

    def display_event_details(self):
        return f"Workshop: {self.title}, Topic: {self.topic}, Date: {self.date}"

    def get_event_type(self):
        return "Workshop"

class SocialEvent(Event):
    activities = models.TextField()

    def display_event_details(self):
        return f"Social Event: {self.title}, Activities: {self.activities}, Date: {self.date}"

    def get_event_type(self):
        return "SocialEvent"
    


    
class Participant(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()


    def __str__(self):
        return self.name
    


# Subclasses of Participant
class Speaker(Participant):
    expertise = models.CharField(max_length=255)


class Attendee(Participant):
    registration_type = models.CharField(max_length=50)


class Organizer(Participant):
    position = models.CharField(max_length=50)


class Volunteer(Participant):
    tasks = models.TextField()


class Registration(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    registration_date = models.DateTimeField(auto_now_add=True)

class Agenda(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='agendas')
    schedule = models.TextField()

    def __str__(self):
        return f"Agenda for {self.event.title}"