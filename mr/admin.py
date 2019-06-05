from django.contrib import admin
from mr.models import *

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(PatientProfile)
admin.site.register(Appointments)
admin.site.register(Vaccination)
admin.site.register(Surgery)
admin.site.register(App_files)
admin.site.register(Prices)
admin.site.register(App_icd10)
admin.site.register(OpeningHours)
admin.site.register(Event)