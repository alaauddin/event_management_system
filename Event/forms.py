from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm




class ConferenceForm(forms.ModelForm):
    class Meta:
        model = Conference
        fields = ['tenant','title', 'location', 'description','discout', 'theme']

class WorkshopForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = ['tenant','title', 'location', 'description',  'discout','topic']

class SocialEventForm(forms.ModelForm):
    class Meta:
        model = SocialEvent
        fields = ['tenant','title', 'location', 'description', 'discout','activities']




class SignUpForm (UserCreationForm):
    class Meta:
        model=User
        fields = {'username','email','password1', 'password2'}