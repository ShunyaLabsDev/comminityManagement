from django import forms
from families.models import Family, Member
from events.models import Event
from announcements.models import Announcement


class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ['family_name', 'village', 'gotra', 'address', 'mobile', 'email', 'business', 'family_photo']
        widgets = {
            'family_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'કુટુંબ નામ / Family Name'}),
            'village': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ગામ / Village'}),
            'gotra': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '98765 43210'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'business': forms.Select(attrs={'class': 'form-select'}),
            'family_photo': forms.FileInput(attrs={'class': 'form-control'}),
        }


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            'name', 'relation', 'gender', 'date_of_birth', 'marital_status',
            'mobile', 'whatsapp', 'email',
            'education', 'education_detail', 'occupation', 'occupation_detail', 'annual_income',
            'blood_group', 'any_disability', 'disability_detail',
            'spouse_name', 'marriage_date',
            'photo',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'નામ / Name'}),
            'relation': forms.Select(attrs={'class': 'form-select'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'marital_status': forms.Select(attrs={'class': 'form-select'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '98765 43210'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'WhatsApp (if different)'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'education': forms.Select(attrs={'class': 'form-select'}),
            'education_detail': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. B.Com Gujarat Uni 2020'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'occupation_detail': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Engineer at TCS, Ahmedabad'}),
            'annual_income': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 3-5 Lakh'}),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'any_disability': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'disability_detail': forms.TextInput(attrs={'class': 'form-control'}),
            'spouse_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Spouse's full name"}),
            'marriage_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        optional = [
            'date_of_birth', 'whatsapp', 'email', 'education', 'education_detail',
            'occupation', 'occupation_detail', 'annual_income', 'blood_group',
            'disability_detail', 'spouse_name', 'marriage_date', 'photo',
        ]
        for f in optional:
            self.fields[f].required = False


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'image', 'event_date', 'event_time', 'location']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'event_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'event_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'description', 'publish_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'publish_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
