from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from .forms import *
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth.models import User
from formtools.wizard.views import SessionWizardView
from django.core.files.storage import DefaultStorage
from django.urls import reverse, reverse_lazy
from datetime import datetime, timedelta
from django.utils.safestring import mark_safe
from .utils import Calendar
import calendar
from bootstrap_modal_forms.generic import BSModalCreateView
from django.utils.timezone import datetime
from django.db.models import Q
from userMessages.models import *



def ehr_index(request):
    return render(request, 'mr/ehr_index.html')


@login_required
def index(request):
    today = datetime.today()
    todays_events = Event.objects.filter(doctor=request.user.userprofile, start_time__year=today.year, start_time__month=today.month, start_time__day=today.day)
    received_messages = Message.objects.filter(receiver=request.user, was_read=False)

    return render(request, 'mr/index.html', {
        "home": "active",
        "todays_events": todays_events,
        "received_messages": received_messages
        })



@csrf_exempt
def register(request):
    context = RequestContext(request)

    registered = False
    if (request.method == 'POST'):
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if (user_form.is_valid() and profile_form.is_valid()):
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True

            user = authenticate(username=user_form.cleaned_data['username'],
                                password=user_form.cleaned_data['password']
                                )
            login(request, user)
        else:
            print (user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response('mr/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered},
        context)




@csrf_exempt
def user_login(request):
    context = RequestContext(request)
    if (request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if (user is not None):
            if user.is_active:
                login(request, user)
                try:
                    UserProfile.objects.get(user__username=username)
                    is_doctor = True
                except UserProfile.DoesNotExist:
                    is_doctor = False

                try:
                    PatientProfile.objects.get(user__username=username)
                    is_patient = True
                except PatientProfile.DoesNotExist:
                    is_patient = False

                if is_doctor:
                    return HttpResponseRedirect('/mr/homepage/')

                if is_patient:
                    return HttpResponseRedirect(reverse("my_mr:my_index"))

            else:
                return HttpResponse("Your account is disabled")
    
        else:
            return HttpResponse("Invalid login details.")

    else:
        return render_to_response('mr/login.html', {}, context)



@csrf_exempt
@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/mr/')



class DetailView(generic.DetailView):
    model = User
    template_name = 'mr/detail.html'

    def get_context_data(self, **kwargs):
        context = {"myprof": "active"}
        context['received_messages'] = Message.objects.filter(receiver=self.request.user, was_read=False)
        return context

    
class DetailUpdate(generic.UpdateView):
    model = UserProfile
    fields = ['specialty', 'city', 'address', 'phone']
    template_name = "mr/detailsUpdate.html"

    def get_success_url(self):
        return reverse('mr:detail', kwargs={'pk': self.object.id})


class UserUpdate(generic.UpdateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']
    template_name = "mr/userUpdate.html"

    def get_success_url(self):
        return reverse('mr:detail', kwargs={'pk': self.object.id})


@csrf_exempt
def register_patient(request):
    context = RequestContext(request)

    registered = False
    if (request.method == 'POST'):
        patient_form = UserForm(data=request.POST)
        patient_profile_form = PatientProfileForm(data=request.POST)

        if (patient_form.is_valid() and patient_profile_form.is_valid()):
            user = patient_form.save()
            user.set_password(user.password)
            user.save()

            profile = patient_profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True

            user = authenticate(username=patient_form.cleaned_data['username'],
                                password=patient_form.cleaned_data['password']
                                )
            login(request, user)
        else:
            print (patient_form.errors, patient_profile_form.errors)
    else:
        patient_form = UserForm()
        patient_profile_form = PatientProfileForm()

    return render_to_response('mr/register_patient.html', {
        'patient_form': patient_form,
        'patient_profile_form': patient_profile_form,
        'registered': registered},
        context)


@csrf_exempt
@login_required
def search_results(request):
    query = request.GET.get("q")
    received_messages = Message.objects.filter(receiver=request.user, was_read=False)

    if query: 
        result_list = PatientProfile.objects.filter(Q(social_security_number__contains=query) | Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query))
    

        return render(request, 'mr/search_results.html', {
            'query': query,
            'result_list': result_list,
            'received_messages': received_messages
            })
            
    else:
        return HttpResponse('Please submit a search term.')
    


class patient_details(generic.DetailView):
    model = PatientProfile
    template_name = 'mr/patient_details.html'

    def get_context_data(self, **kwargs):
        context = super(patient_details, self).get_context_data(**kwargs)
        self.request.session['p_id'] = self.kwargs['pk']
        context['p_id'] = self.request.session['p_id']
        context['received_messages'] = Message.objects.filter(receiver=self.request.user, was_read=False)
        return context



@csrf_exempt
@login_required
def add_appointment(request):
    template_name = 'mr/add_appointment.html'
    p_id = request.session.get('p_id')
    complete = False
    received_messages = Message.objects.filter(receiver=request.user, was_read=False)

    if (request.method == 'POST'):
        appointments_form = AppointmentsForm(data=request.POST)
        
        if (appointments_form.is_valid()):
            appointments = appointments_form.save()            
            appointments.save()
            
            request.session['current_app_id'] = appointments.id
            complete = True
        else:
            print(appointments_form.errors)
    else:
        default_patient = PatientProfile.objects.get(id=p_id)
        default_doctor = UserProfile.objects.get(id=request.user.userprofile.id)
        
        appointments_form = AppointmentsForm(initial={
            "patient": default_patient,
            "doctor": default_doctor
        })

    
    return render(request, template_name, {
        'appointments_form': appointments_form,
        'complete': complete,
        'p_id': p_id,
        'received_messages': received_messages
        })



def add_icd10_codes(request):
    template_name = 'mr/add_icd10_codes.html'
    p_id = request.session.get('p_id')
    complete = False
    received_messages = Message.objects.filter(receiver=request.user, was_read=False)

    if (request.method == "POST"):
        app_icd10_form =  App_icd10Form(data=request.POST)

        if (app_icd10_form.is_valid()):
            app_icd10 = app_icd10_form.save(commit=False)
            app_icd10.icd10_code = request.POST.get('myInput')
            app_icd10.save()

            if not request.POST.get('checkbox'):
                complete = True
            else:
                complete = False

        else:
            print(app_icd10_form.errors)

    else:
        default_app = Appointments.objects.get(id=request.session.get('current_app_id'))

        app_icd10_form = App_icd10Form(initial={
            "appointment": default_app
        })
    
    icd_list = App_icd10.objects.filter(appointment__id=request.session.get('current_app_id'))

    return render(request, template_name, {
        'app_icd10_form': app_icd10_form,
        'complete': complete,
        'icd_list': icd_list,
        'p_id': p_id,
        'received_messages': received_messages
    })



def icd10Add(request):
    template_name = 'mr/update_icd10_codes.html'
    p_id = request.session.get('p_id')
    complete = False
    received_messages = Message.objects.filter(receiver=request.user, was_read=False)

    if (request.method == "POST"):
        app_icd10_form =  App_icd10Form(data=request.POST)

        if (app_icd10_form.is_valid()):
            app_icd10 = app_icd10_form.save(commit=False)
            app_icd10.icd10_code = request.POST.get('myInput')
            app_icd10.save()

            if not request.POST.get('checkbox'):
                complete = True
            else:
                complete = False

        else:
            print(app_icd10_form.errors)

    else:
        default_app = Appointments.objects.get(id=request.session.get('app_id'))

        app_icd10_form = App_icd10Form(initial={
            "appointment": default_app
        })
    
    icd_list = App_icd10.objects.filter(appointment__id=request.session.get('app_id'))

    return render(request, template_name, {
        'app_icd10_form': app_icd10_form,
        'complete': complete,
        'icd_list': icd_list,
        'p_id': p_id,
        'app_id': request.session.get('app_id'),
        'received_messages': received_messages
    })



@csrf_exempt
@login_required
def add_vaccination(request):
    template_name = 'mr/add_vaccination.html'
    p_id = request.session.get('p_id')
    registered = False
    received_messages = Message.objects.filter(receiver=request.user, was_read=False)

    if (request.method == 'POST'):
        vaccination_form = VaccinationForm(data=request.POST)
        
        if (vaccination_form.is_valid()):
            vaccination = vaccination_form.save()
            vaccination.save()
        
            registered = True
        else:
            print(vaccination_form.errors)
    else:
        default_patient = PatientProfile.objects.get(id=p_id)
        default_doctor = UserProfile.objects.get(id=request.user.userprofile.id)

        vaccination_form = VaccinationForm(initial={
            "patient": default_patient,
            "doctor": default_doctor
        })

    return render(request, template_name, {
        'vaccination_form': vaccination_form,
        'registered': registered,
        'p_id': p_id,
        'received_messages': received_messages
        })



@csrf_exempt
@login_required
def add_surgery(request):
    template_name = 'mr/add_surgery.html'
    p_id = request.session.get('p_id')
    registered = False
    received_messages = Message.objects.filter(receiver=request.user, was_read=False)

    if (request.method == 'POST'):
        surgery_form = SurgeryForm(data=request.POST)

        if (surgery_form.is_valid()):
            surgery = surgery_form.save()
            surgery.save()

            request.session['current_surgery_id'] = surgery.id
            registered = True
        else:
            print (surgery_form.errors)
    else:
        default_patient = PatientProfile.objects.get(id=p_id)
        default_doctor = UserProfile.objects.get(id=request.user.userprofile.id)

        surgery_form = SurgeryForm(initial={
            "patient": default_patient,
            "doctor": default_doctor
        })
        

    return render(request, template_name, {
        'surgery_form': surgery_form,
        'registered': registered,
        'p_id': p_id,
        'received_messages': received_messages
        })



@csrf_exempt
@login_required
def add_app_file(request):
    template_name = 'mr/add_file.html'
    p_id = request.session.get('p_id')
    complete = False
    received_messages = Message.objects.filter(receiver=request.user, was_read=False)

    if (request.method == 'POST'):
        file_form = AppFileForm(request.POST, request.FILES)

        if(file_form.is_valid()):
            new_file = file_form.save()
            new_file.save()

            if not request.POST.get('checkbox'):
                complete = True
            else:
                complete = False
        else:
            print (file_form.errors)
    else:
        default_app =  Appointments.objects.get(id=request.session.get('current_app_id'))

        file_form = AppFileForm(initial={"appointment": default_app})

    return render(request, template_name, {
        'file_form': file_form,
        'complete': complete,
        'p_id': p_id,
        'received_messages': received_messages})




@csrf_exempt
@login_required
def add_surgery_file(request):
    template_name = 'mr/add_file.html'
    p_id = request.session.get('p_id')
    complete = False
    received_messages = Message.objects.filter(receiver=request.user, was_read=False)

    if (request.method == 'POST'):
        file_form = SurgeryFileForm(request.POST, request.FILES)

        if(file_form.is_valid()):
            new_file = file_form.save()
            new_file.save()

            if not request.POST.get('checkbox'):
                complete = True
            else:
                complete = False
        else:
            print (file_form.errors)
    else:
        default_app =  Surgery.objects.get(id=request.session.get('current_surgery_id'))

        file_form = AppFileForm(initial={"appointment": default_app})

    return render(request, template_name, {
        'file_form': file_form,
        'complete': complete,
        'p_id': p_id,
        'received_messages': received_messages})




class appointments_list(generic.ListView):
    context_object_name = 'appointments_list'
    template_name = 'mr/appointments_list.html'
    paginate_by = 15

    def get_queryset(self, **kwargs):
        p_id = self.request.session.get('p_id')
        return Appointments.objects.filter(patient__id=p_id).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super(appointments_list, self).get_context_data(**kwargs)
        context['received_messages'] = Message.objects.filter(receiver=self.request.user, was_read=False)
        return context



class appointments_detail(generic.DetailView):
    model = Appointments
    template = 'mr/app_details.html'

    def get_context_data(self, **kwargs):
        context = super(appointments_detail, self).get_context_data(**kwargs)
        self.request.session['app_id'] = self.kwargs['pk']
        context['icd10_list'] = App_icd10.objects.filter(appointment__id=self.kwargs['pk'])
        context['app_files'] = App_files.objects.filter(appointment__id=self.kwargs['pk'])
        context['received_messages'] = Message.objects.filter(receiver=self.request.user, was_read=False)
        return context



class vaccinations_list(generic.ListView):
    context_object_name = 'vaccinations_list'
    template_name = 'mr/vaccinations_list.html'
    paginate_by = 15

    def get_queryset(self):
        p_id = self.request.session.get('p_id')
        return Vaccination.objects.filter(patient__id=p_id).order_by('-date')
    
    def get_context_data(self, **kwargs):
        context = super(vaccinations_list, self).get_context_data(**kwargs)
        context['received_messages'] = Message.objects.filter(receiver=self.request.user, was_read=False)
        return context



class vaccination_detail(generic.DetailView):
    model = Vaccination
    template = 'mr/vaccination_detail.html'

    def get_context_data(self, **kwargs):
        context = super(vaccination_detail, self).get_context_data(**kwargs)
        context['received_messages'] = Message.objects.filter(receiver=self.request.user, was_read=False)
        return context



class surgeries_list(generic.ListView):
    context_object_name = 'surgeries_list'
    template_name = 'mr/surgeries_list.html'
    paginate_by = 15

    def get_queryset(self):
        p_id = self.request.session.get('p_id')
        return Surgery.objects.filter(patient__id=p_id).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super(surgeries_list, self).get_context_data(**kwargs)
        context['received_messages'] = Message.objects.filter(receiver=self.request.user, was_read=False)
        return context



class surgery_detail(generic.DetailView):
    model = Surgery
    template = 'mr/surgery_detail.html'

    def get_context_data(self, **kwargs):
        context = super(surgery_detail, self).get_context_data(**kwargs)
        context['received_messages'] = Message.objects.filter(receiver=self.request.user, was_read=False)
        return context


class SurgeryDelete(generic.DeleteView):
     model = Surgery
     success_url = reverse_lazy('mr:surgeries_list')   


class SurgeryUpdate(generic.UpdateView):
    model = Surgery
    fields = ['date', 'procedure_description', 'result_description', 'medication', 'side_effects', 'secret_note']
    template_name = "mr/update_surgery.html"

    def get_success_url(self):
        return reverse('mr:surgery_detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(SurgeryUpdate, self).get_context_data(**kwargs)
        context['received_messages'] = Message.objects.filter(receiver=self.request.use, was_read=Falser)
        return context



class AppointmentUpdate(generic.UpdateView):
    model = Appointments
    fields = ['date', 'symptoms_description', 'diagnosis', 'examination_description', 'medication', 'medication_side_effects', 'secret_note']
    template_name = "mr/update_appointment.html"

    def get_success_url(self):
        return reverse('mr:appointments_detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(AppointmentUpdate, self).get_context_data(**kwargs)
        context['received_messages'] = Message.objects.filter(receiver=self.request.user, was_read=False)
        return context



class AppointmentDelete(generic.DeleteView):
    model = Appointments
    success_url = reverse_lazy('mr:appointments_list')



class VaccinationDelete(generic.DeleteView):
    model = Vaccination
    success_url = reverse_lazy('mr:vaccinations_list')



class VaccinationUpdate(generic.UpdateView):
    model = Vaccination
    fields = ['date', 'description', 'side_effects', 'secret_note']
    template_name = "mr/update_vaccination.html"

    def get_success_url(self):
        return reverse('mr:vaccination_detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(VaccinationUpdate, self).get_context_data(**kwargs)
        context['received_messages'] = Message.objects.filter(receiver=self.request.user, was_read=False)
        return context



class price_list(generic.ListView):
    context_object_name = 'price_list'
    template_name = 'mr/price_list.html'

    def get_queryset(self):
        return Prices.objects.filter(doctor__id=self.request.user.userprofile.id)

    def get_context_data(self, **kwargs):
        context = super(price_list, self).get_context_data(**kwargs)
        context['received_messages'] = Message.objects.filter(receiver=self.request.user, was_read=False)
        return context




class icd10Delete(generic.DeleteView):
    model = App_icd10
   
    def get_success_url(self):
        app_id = self.request.session.get('app_id')
        return reverse('mr:appointments_detail', kwargs={'pk': app_id})



@csrf_exempt
@login_required
def add_price(request):
    template_name = 'mr/add_price.html'
    added = False
    if (request.method == 'POST'):
        price_form = PriceForm(data=request.POST)

        if (price_form.is_valid()):
            price = price_form.save()
            price.save()

            added = True
        else:
            print (price_form.errors)
    else:
        
        default_doctor = UserProfile.objects.get(id=request.user.userprofile.id)
        price_form = PriceForm(initial={"doctor": default_doctor})
    
    received_messages = Message.objects.filter(receiver=request.user, was_read=False)
    return render(request, template_name, {
        'price_form': price_form,
        'added': added,
        'received_messages': received_messages
        })


class PriceDelete(generic.DeleteView):
    model = Prices
    success_url = reverse_lazy('mr:price_list')



class opening_hours(generic.ListView):
    context_object_name = 'opening_hours'
    template_name = 'mr/opening_hours.html'

    def get_queryset(self):
        return OpeningHours.objects.filter(doctor__id=self.request.user.userprofile.id)

    def get_context_data(self, **kwargs):
        context = super(opening_hours, self).get_context_data(**kwargs)
        context['received_messages'] = Message.objects.filter(receiver=self.request.user, was_read=False)
        return context


class OpeningHoursDelete(generic.DeleteView):
    model = OpeningHours
    success_url = reverse_lazy('mr:opening_hours')



@csrf_exempt
@login_required
def add_opening_hours(request):
    template_name = 'mr/add_opening_hours.html'
    added = False
    if (request.method == 'POST'):
        opening_hours_form = OpeningHoursForm(data=request.POST)

        if (opening_hours_form.is_valid()):
            hours = opening_hours_form.save()
            hours.save()

            added = True
        else:
            print (opening_hours_form.errors)

    else:

        default_doctor = UserProfile.objects.get(id=request.user.userprofile.id)
        opening_hours_form = OpeningHoursForm(initial={"doctor": default_doctor})

    received_messages = Message.objects.filter(receiver=request.user, was_read=False)
    return render(request, template_name, {
        'opening_hours_form': opening_hours_form,
        'added': added,
        'received_messages': received_messages
    })



class CalendarView(generic.ListView):
    model = Event
    template_name = 'mr/calendar.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        d = get_date(self.request.GET.get('day', None))
        d = get_date(self.request.GET.get('month', None))
        my_id = self.request.user.userprofile.id
        # Instantiate the calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method which returns the calendar as table
        html_cal = cal.formatmonth(my_id, withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['received_messages'] = Message.objects.filter(receiver=self.request.user, was_read=False)
        return context

        

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


@csrf_exempt
@login_required
def new_event(request):
    template_name = 'mr/new_event.html'
    added = False
    query = request.POST.get("q")
    search = True
    event_form = EventForm(data=request.POST)

    if (request.method == "POST"):
        if ('search' in request.POST):
            search = False
            result_list = PatientProfile.objects.filter(Q(social_security_number__contains=query) | Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query))
            added = False

            default_doctor = UserProfile.objects.get(id=request.user.userprofile.id)
            event_form = EventForm(initial={
                "doctor": default_doctor
            })
            

            return render(request, template_name, {
                'search': search,
                'added': added,
                'event_form': event_form,
                'result_list': result_list
            })
            
        elif ('submit' in request.POST):
            if (event_form.is_valid()):
                event = event_form.save(commit=False)

                default_patient = PatientProfile.objects.get(id=request.POST.get("patient"))
                event.patient = default_patient
                event.save()
                added = True
                search = False
            else:
                print (event_form.errors)
    
    received_messages = Message.objects.filter(receiver=request.user, was_read=False)
    return render(request, template_name, {
        'search': search,
        'added': added,
        'event_form': event_form,
        'received_messages': received_messages
    })
    

    





#ctrl+K & ctrl+C adds #
#ctrl+K & ctrl+U removes #
# def edit_event(request, event_id=None):
#     instance = Event()
#     if event_id:
#         instance = get_object_or_404(Event, pk=event_id)

#         event = Event.objects.get(id=event_id)
#         form = EventForm(instance=instance)
#         return render(request, 'mr/event.html', {
#             'form': form,
#             'event': event
#         })
#     else:
#         return HttpResponse('Something went wrong.')
        

class EventUpdate(generic.UpdateView):
    model = Event
    fields = ['description', 'start_time', 'confirmed', 'cost']
    template_name = "mr/event.html"
    
    def get_success_url(self):
        return reverse('mr:calendar')

    def get_context_data(self, **kwargs):
        context = super(EventUpdate, self).get_context_data(**kwargs)
        context['received_messages'] = Message.objects.filter(receiver=self.request.user, was_read=False)
        return context



class EventDelete(generic.DeleteView):
    model = Event
    success_url = reverse_lazy('mr:calendar')



class DoctorDetail(generic.DetailView):
    model = UserProfile
    template_name = 'mr/doctor_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DoctorDetail, self).get_context_data(**kwargs)
        context['prices_list'] = Prices.objects.filter(doctor__id=self.kwargs['pk'])
        context['opening_hours_list'] = OpeningHours.objects.filter(doctor__id=self.kwargs['pk'])
        context['received_messages'] = Message.objects.filter(receiver=self.request.user, was_read=False)
        return context



class InboxList(generic.ListView):
    context_object_name = 'inbox_list'
    template_name = 'mr/messages.html'
    paginate_by = 15

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super(InboxList, self).get_context_data(**kwargs)
        context['type'] = 'inbox'
        context['received_messages'] = Message.objects.filter(receiver=self.request.user, was_read=False)
        return context


class MessageDelete(generic.DeleteView):
    model = Message

    def get_success_url(self):
        return self.request.POST.get('url')
        


class SentList(generic.ListView):
    context_object_name = 'sent_list'
    template_name = 'mr/messages.html'
    paginate_by = 15

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super(SentList, self).get_context_data(**kwargs)
        context['type'] = 'sent'
        context['received_messages'] = Message.objects.filter(receiver=self.request.user, was_read=False)
        return context