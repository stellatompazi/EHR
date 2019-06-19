from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
import os

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    specialties_list = (
        ('Accident_and_Emergency_Medicine', 'Accident and Emergency Medicine'),
        ('Allergiology', 'Allergiology'),
        ('Anesthetics', 'Anesthetics'),
        ('Cardiology', 'Cardiology'),
        ('Child_Psychiatry', 'Child Psychiatry'),
        ('Clinical_Biology', 'Clinical Biology'),
        ('Clinical_Chemistry', 'Clinical Chemistry'),
        ('Clinical_Neurophysiology', 'Clinical Neurophysiology'),
        ('Dental_Oral_Maxillo-facial_surgery', 'Dental, Oral and Maxillo-facial Surgery'),
        ('Dermato-Venereology', 'Dermato-Venereology'),
        ('Dermatology', 'Dermatology'),
        ('Endocrinology', 'Endocrinology'),
        ('Family_and_general_Medicine', 'Family and General Medicine'),
        ('Fictional_Medical_Specialist', 'Fictional Medical Specialist'),
        ('Gastro-enterologic_Surgery', 'Gastro-enterologic Surgery'),
        ('Gastroenterology', 'Gastroenterology'),
        ('General_Hematology', 'General Hematology'),
        ('General_Practice', 'General Practice'),
        ('General_Surgery', 'General Surgery'),
        ('Geriatrics', 'Geriatrics'),
        ('Immunology', 'Immunology'),
        ('Infectious_Diseases', 'Infectious Diseases'),
        ('Internal_Medicine', 'Internal Medicine'),
        ('Laboratory_Medicine', 'Laboratory Medicine'),
        ('Maxillo-facial_Surgery', 'Maxillo-facial Surgery'),
        ('Microbiology', 'Microbiology'),
        ('Nephrology', 'Nephrology'),
        ('Neuro-psychiatry', 'Neuro-psyciatry'),
        ('Neurosurgery', 'Neurosurgery'),
        ('Nuclear_Medicine', 'Nuclear Medicine'),
        ('Obstetrics_and_Gynecology', 'Obstetrics and Gynecology'),
        ('Occupational_Medicine', 'Occupational Medicine'),
        ('Opthalmology', 'Ophtalmology'),
        ('Orthopaedics', 'Orthopaedics'),
        ('Otorhinolaryngology', 'Otorhinolaryngology'),
        ('Paediatrics', 'Paediatrics'),
        ('Paediatrics_Surgery', 'Paediatrics Surgery'),
        ('Pathology', 'Pathology'),
        ('Physical_Medicine_and_Rehabilitation', 'Physical Medicine and Rehabilitation'),
        ('Plastic_Surgery', 'Plastic Surgery'),
        ('Pneumology', 'Pneumology'),
        ('Podiatric_Surgery', 'Podiatric Surgery'),
        ('Psychiatry', 'Psychiatry'),
        ('Public_health_and_Preventive_Medicine', 'Public Health and Preventive Medicine'),
        ('Radiation_Oncology', 'Radiation Oncology'),
        ('Respiratory_Medicine', 'Respiratory Medicine'),
        ('Rheumatogoly', 'Rheumatology'),
        ('Stomatology', 'Stomatology'),
        ('Thoragic_Surgery', 'Thoragic Surgery'),
        ('Tropical_Medicine', 'Tropical Medicine'),
        ('Urology', 'Urology'),
        ('Vascular_Surgery', 'Vascular Surgery'),
        ('Venereology', 'Venereology')
    )

    
    specialty = models.CharField(max_length=100, choices=specialties_list, default='General_Practice')
    city = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=12, blank=True)

    def __str__(self):
        return self.user.username + ' - ' + self.specialty


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    birthday = models.DateField(null=True)
    social_security_number = models.CharField(max_length=11, unique=True)
    gender = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    sex = models.CharField(max_length=6, choices=gender, default='Male')
    insurance = models.CharField(max_length=100, blank=True)

    blood_type = (
        ('Ο-', 'Ο-'),
        ('Ο+', 'Ο+'),
        ('Α-', 'Α-'),
        ('Α+', 'Α+'),
        ('Β-', 'Β-'),
        ('Β+', 'Β+'),
        ('ΑΒ-', 'ΑΒ-'),
        ('ΑΒ+', 'ΑΒ+'),
    )
    blood = models.CharField(max_length=3, choices=blood_type, default='')
    city = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=12, blank=True)

    def __str__(self):
        return self.user.username


class Appointments(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    date = models.DateField(null=False, default=date.today)

    symptoms_description = models.CharField(max_length=1000, blank=True)

    diagnosis = models.CharField(max_length=2000, default='None')
    
    examination_description = models.CharField(max_length=5000, default='None')

    medication = models.CharField(max_length=500, blank=True)
    medication_side_effects = models.CharField(max_length=1000, blank=True)

    secret_note = models.CharField(max_length=1000, blank=True)

    def __str__(self):
       return self.patient.user.username + ' - ' + self.doctor.specialty + ' - id: ' + str(self.id)


class App_icd10(models.Model):
    appointment = models.ForeignKey(Appointments, on_delete=models.CASCADE)

    icd10_code = models.CharField(max_length=1000, blank=False)

    def __str__(self):
        return self.appointment.patient.user.username + ' - ' + self.icd10_code
        


class Vaccination(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    date = models.DateField(null=False, default=date.today)
    description = models.CharField(max_length=500, blank=True)
    side_effects = models.CharField(max_length=1000, blank=True)
    secret_note = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.patient.user.username + ' - ' + self.doctor.specialty


class Surgery(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    date = models.DateField(null=False, default=date.today)
    procedure_description = models.CharField(max_length=5000, blank=True)
    result_description = models.CharField(max_length=5000, blank=True)
    medication = models.CharField(max_length=500, blank=True)
    side_effects = models.CharField(max_length=1000, blank=True)
    secret_note = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.patient.user.username + ' - ' + self.doctor.specialty


class App_files(models.Model):
    appointment = models.ForeignKey(Appointments, on_delete=models.CASCADE)
    upload = models.FileField(upload_to='exam_files/')

    def __str__(self):
        return self.upload.name


class Surgery_files(models.Model):
    surgery = models.ForeignKey(Surgery, on_delete=models.CASCADE)
    upload = models.FileField(upload_to='exam_files/')

    def __str__(self):
        return self.appointment.patient.user.username


class Prices(models.Model):
    doctor = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    name = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=5000, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.IntegerField(default=15, validators=[MaxValueValidator(300), MinValueValidator(1)])
    
    def __str__(self):
        return self.doctor.user.username + ' - ' + self.name




class OpeningHours(models.Model):
    doctor = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    WEEKDAYS = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday')
    )

    day = models.IntegerField(choices=WEEKDAYS)
    from_hour = models.TimeField()
    to_hour = models.TimeField()

    class Meta:
        ordering = ('day', 'from_hour')
        unique_together = ('doctor', 'day', 'from_hour', 'to_hour')

    def __unicode__(self):
        return u'%s: %s - %s' % (self.get_day_display(),
                                 self.from_hour, self.to_hour)


class Event(models.Model):
    doctor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, null=True)

    description = models.TextField()
    start_time = models.DateTimeField()
    confirmed = models.BooleanField(default=False)
    cost = models.DecimalField(max_digits=8, decimal_places=2)

    def __unicode__(self):
        return patient_name, start_time

    @property
    def get_html_url(self):
        url = reverse('mr:edit_event', args=(self.id,))
        return f'<a href="{url}"> {self.start_time.time()} - {self.patient.user.get_full_name()} </a>'


class Favourites(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return  self.patient.user.username + ' - ' + self.doctor.user.username