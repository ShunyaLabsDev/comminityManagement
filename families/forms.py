from django import forms
from .models import Family, Member


class UserFamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ['family_name', 'village', 'gotra', 'address', 'mobile', 'email', 'business', 'family_photo']
        widgets = {
            'family_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. કનુભાઈ મગનભાઈ પટેલ'}),
            'village': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. હિંમતનગર'}),
            'gotra': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full address with taluka, district, pincode'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '98765 43210'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'family@example.com (optional)'}),
            'business': forms.Select(attrs={'class': 'form-select'}),
            'family_photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = False
        self.fields['family_photo'].required = False


class UserMemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            # Basic
            'name', 'relation', 'gender', 'date_of_birth', 'marital_status',
            # Contact
            'mobile', 'whatsapp', 'email',
            # Education & Work
            'education', 'education_detail', 'occupation', 'occupation_detail', 'annual_income',
            # Health
            'blood_group', 'any_disability', 'disability_detail',
            # Marriage
            'spouse_name', 'marriage_date',
            # Photo
            'photo',
        ]
        widgets = {
            # Basic
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name (ગુજરાતી or English)'}),
            'relation': forms.Select(attrs={'class': 'form-select'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'marital_status': forms.Select(attrs={'class': 'form-select'}),
            # Contact
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '98765 43210'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'WhatsApp number (if different)'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'member@example.com'}),
            # Education
            'education': forms.Select(attrs={'class': 'form-select'}),
            'education_detail': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. B.Com from Gujarat University, 2020'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Farmer, Engineer, Student'}),
            'occupation_detail': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Software Engineer at TCS, Ahmedabad'}),
            'annual_income': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 3-5 Lakh'}),
            # Health
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'any_disability': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'disability_detail': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief description if applicable'}),
            # Marriage
            'spouse_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Spouse's full name"}),
            'marriage_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            # Photo
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # All optional except name, relation, gender
        optional = [
            'date_of_birth', 'mobile', 'whatsapp', 'email',
            'education', 'education_detail', 'occupation', 'occupation_detail', 'annual_income',
            'blood_group', 'disability_detail', 'spouse_name', 'marriage_date', 'photo',
        ]
        for f in optional:
            self.fields[f].required = False
