from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
import re




from django import forms
def is_yemeni_phone_number(phone):
    # Check if the phone number follows the Yemeni format
    # You can customize this regex based on the actual format used in Yemen
    yemeni_phone_regex = re.compile(r'^\+967\d{9}$')

    return bool(yemeni_phone_regex.match(phone))




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

class AttendeeRegistrationForm(forms.ModelForm):
    class Meta:
        model = Attendee
        fields = ['name', 'email', 'phone', 'organization']

    def __init__(self, *args, **kwargs):
        super(AttendeeRegistrationForm, self).__init__(*args, **kwargs)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not is_yemeni_phone_number(phone):
            raise forms.ValidationError("Please enter a valid Yemeni phone number.")
        return phone


class VolunteerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['name', 'email', 'phone', 'tasks']

    def __init__(self, *args, **kwargs):
        super(VolunteerRegistrationForm, self).__init__(*args, **kwargs)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not is_yemeni_phone_number(phone):
            raise forms.ValidationError("Please enter a valid Yemeni phone number.")
        return phone


class SpeakerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Speaker
        fields = ['name', 'email', 'expertise']

    def __init__(self, *args, **kwargs):
        super(SpeakerRegistrationForm, self).__init__(*args, **kwargs)


class OrganizerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Organizer
        fields = ['name', 'email', 'position']

    def __init__(self, *args, **kwargs):
        super(OrganizerRegistrationForm, self).__init__(*args, **kwargs)






class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'capacity', 'price']


class SignUpForm (UserCreationForm):
    class Meta:
        model=User
        fields = {'username','email','password1', 'password2'}