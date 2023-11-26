from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm



from django import forms

class ConferenceForm(forms.ModelForm):
    class Meta:
        model = Conference
        fields = ['tenant', 'title', 'location', 'description', 'discout', 'theme', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class WorkshopForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = ['tenant', 'title', 'location', 'description', 'discout', 'topic', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class SocialEventForm(forms.ModelForm):
    class Meta:
        model = SocialEvent
        fields = ['tenant', 'title', 'location', 'description', 'discout', 'activities', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }



class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'capacity', 'price']


class SignUpForm (UserCreationForm):
    class Meta:
        model=User
        fields = {'username','email','password1', 'password2'}