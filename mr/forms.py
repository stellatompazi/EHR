from django import forms
from mr.models import *
from django.contrib.auth.models import User
from bootstrap_modal_forms.forms import BSModalForm


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('specialty', 'city', 'address', 'phone')


class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ('birthday', 'social_security_number', 'sex', 'insurance', 'blood', 'city', 'address', 'phone')
 

class AppointmentsForm(forms.ModelForm):
    class Meta:
        model = Appointments
        fields = ('patient', 'doctor', 'date', 'symptoms_description', 'diagnosis', 'examination_description', 'medication', 'medication_side_effects', 'secret_note')
        widgets = {
            'patient': forms.HiddenInput(),
            'doctor': forms.HiddenInput(),
            'date': forms.DateInput(attrs={'type': 'date'}, format= '%d-%b-%Y')
            }

class App_icd10Form(forms.ModelForm):
    class Meta:
        model = App_icd10
        fields = ('appointment',)
        widgets = {
            'appointment': forms.HiddenInput()
            }

class AppFileForm(forms.ModelForm):
    class Meta:
        model = App_files
        fields = ('appointment', 'upload')
        widgets = {
            'appointment': forms.HiddenInput()
        }


class SurgeryFileForm(forms.ModelForm):
    class Meta:
        model = Surgery_files
        fields = ('surgery', 'upload')


class VaccinationForm(forms.ModelForm):
    class Meta:
        model = Vaccination
        fields = ('patient', 'doctor', 'date' ,'description', 'side_effects', 'secret_note')
        widgets = {
            'patient': forms.HiddenInput(),
            'doctor': forms.HiddenInput()
            }


class SurgeryForm(forms.ModelForm):
    class Meta:
        model = Surgery
        fields = ('patient', 'doctor', 'date', 'procedure_description', 'result_description', 'medication', 'side_effects', 'secret_note')
        widgets = {
            'patient': forms.HiddenInput(),
            'doctor': forms.HiddenInput()
            }


class PriceForm(forms.ModelForm):
    class Meta:
        model = Prices
        fields = ('doctor', 'name', 'description', 'price', 'duration')
        widgets = {
            'doctor': forms.HiddenInput()
            }


class OpeningHoursForm(forms.ModelForm):
    class Meta:
        model = OpeningHours
        fields = ('doctor', 'day', 'from_hour', 'to_hour')
        widgets = {
            'doctor': forms.HiddenInput(),
            'from_hour': forms.TimeInput(format='%H:%M'),
            'to_hour': forms.TimeInput(format='%H:%M')
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        #fields = '__all__'
        fields = ('doctor', 'description', 'start_time', 'confirmed', 'cost')
        widgets = {
            'start_time': forms.DateInput(attrs={'type': 'datetime-local'}, format= '%d-%m-%Y T%H:%M'),
            'doctor': forms.HiddenInput(),
            'patient': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
