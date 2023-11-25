from django import forms
from .models import *



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


        