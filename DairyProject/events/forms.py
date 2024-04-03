from django import forms
from .models import Meeting, MeetingDetails

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['title', 'date', 'time', 'location', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
class MeetingDetailsForm(forms.ModelForm):
    class Meta:
        model = MeetingDetails
        fields = ['meeting', 'attendees', 'agenda', 'description']