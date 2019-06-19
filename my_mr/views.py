from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import generic
from mr.models import *
from django.contrib.auth.decorators import login_required
from django.utils.timezone import datetime
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from userMessages.models import *
from django.urls import reverse, reverse_lazy



# Create your views here.
def index(request):
    today = datetime.today()
    future_events = Event.objects.filter(patient=request.user.patientprofile, start_time__gte=today)
    received_messages = Message.objects.filter(receiver=request.user, was_read=False)
    
    return render(request, 'my_mr/my_index.html', {
        'nbar': 'active',
        'future_events': future_events,
        'received_messages': received_messages
        })



class DetailView(generic.DetailView):
    model = User
    template_name = 'my_mr/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['myprof'] = 'active'
        context['received_messages'] = Message.objects.filter(receiver=self.request.user, was_read=False)
        return context



class DetailUpdate(generic.UpdateView):
    model = PatientProfile
    fields = ['birthday', 'social_security_number', 'sex', 'insurance', 'blood', 'city', 'address', 'phone']
    template_name = "my_mr/detailsUpdate.html"
    
    def get_success_url(self):
        return reverse('my_mr:detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(DetailUpdate, self).get_context_data(**kwargs)
        context['myprof'] = 'active'
        context['received_messages'] = Message.objects.filter(receiver=self.request.user, was_read=False)
        return context




class UserUpdate(generic.UpdateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']
    template_name = "my_mr/userUpdate.html"

    
    def get_success_url(self):
        return reverse('my_mr:detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(UserUpdate, self).get_context_data(**kwargs)
        context['myprof'] = 'active'
        context['received_messages'] = Message.objects.filter(receiver=self.request.user, was_read=False)
        return context


class appointments_list(generic.ListView):
    template_name = 'my_mr/appointments_list.html'
    paginate_by = 15

    def get_queryset(self):
        return Appointments.objects.filter(patient__user__username=self.request.user.username).order_by('-date')
    
    def get_context_data(self, **kwargs):
        context = super(appointments_list, self).get_context_data(**kwargs)
        context['received_messages'] = Message.objects.filter(receiver=self.request.user, was_read=False)
        return context



class app_detail(generic.DetailView):
    model = Appointments
    template_name = 'my_mr/app_detail.html'

    def get_context_data(self, **kwargs):
        context = super(app_detail, self).get_context_data(**kwargs)
        context['received_messages'] = Message.objects.filter(receiver=self.request.user, was_read=False)
        context['icd10_list'] = App_icd10.objects.filter(appointment__id=self.kwargs['pk'])
        return context



class vaccinations_list(generic.ListView):
    context_object_name = 'vaccinations_list'
    template_name = 'my_mr/vaccinations_list.html'
    paginate_by = 15

    def get_queryset(self):
        return Vaccination.objects.filter(patient__user__username=self.request.user.username)
        
    def get_context_data(self, **kwargs):
        context = super(vaccinations_list, self).get_context_data(**kwargs)
        context['received_messages'] = Message.objects.filter(receiver=self.request.user, was_read=False)
        return context



class vaccination_detail(generic.DetailView):
    model = Vaccination
    template_name = 'my_mr/vaccination_detail.html'

    def get_context_data(self, **kwargs):
        context = super(vaccination_detail, self).get_context_data(**kwargs)
        context['received_messages'] = Message.objects.filter(receiver=self.request.user, was_read=False)
        return context



class surgeries_list(generic.ListView):
    context_object_name = 'surgeries_list'
    template_name = 'my_mr/surgeries_list.html'
    paginate_by = 15

    def get_queryset(self):
        return Surgery.objects.filter(patient__user__username=self.request.user.username)
    
    def get_context_data(self, **kwargs):
        context = super(surgeries_list, self).get_context_data(**kwargs)
        context['received_messages'] = Message.objects.filter(receiver=self.request.user, was_read=False)
        return context



class surgery_detail(generic.DetailView):
    model = Surgery
    template_name = 'my_mr/surgery_detail.html'

    def get_context_data(self, **kwargs):
        context = super(surgery_detail, self).get_context_data(**kwargs)
        context['received_messages'] = Message.objects.filter(receiver=self.request.user, was_read=False)
        return context



def specialties(request):
    received_messages = Message.objects.filter(receiver=request.user, was_read=False)
    return render(request, 'my_mr/specialties.html', {
        'specialties': UserProfile.specialties_list,
        'received_messages': received_messages
        })



class doctor_list(generic.ListView):
    context_object_name = 'doctor_list'
    template_name = 'my_mr/doctor_list.html'
    paginate_by = 15

    def get_queryset(self, *args, **kwargs):
        q = self.kwargs['slug']
        return UserProfile.objects.filter(specialty=q)

    def get_context_data(self, **kwargs):
        context = super(doctor_list, self).get_context_data(**kwargs)
        context['specialties'] = True
        context['received_messages'] = Message.objects.filter(receiver=self.request.user, was_read=False)
        return context



class doctor_detail(generic.DetailView):
    model = UserProfile
    template_name = 'my_mr/doctor_detail.html'

    def get_context_data(self, **kwargs):
        context = super(doctor_detail, self).get_context_data(**kwargs)
        context['price_list'] = Prices.objects.filter(doctor__id=self.kwargs['pk'])
        context['opening_hours_list'] = OpeningHours.objects.filter(doctor__id=self.kwargs['pk'])
        context['is_favourite'] = Favourites.objects.filter(patient=self.request.user.patientprofile, doctor__id=self.kwargs['pk'])
        context['specialties'] = True
        context['received_messages'] = Message.objects.filter(receiver=self.request.user, was_read=False)
        return context



class FavouritesList(generic.ListView):
    context_object_name = 'favourites'
    template_name = 'my_mr/favourites.html'
    paginate_by = 15

    def get_queryset(self):
        return Favourites.objects.filter(patient=self.request.user.patientprofile).order_by('doctor__specialty')

    def get_context_data(self, **kwargs):
        context = super(FavouritesList, self).get_context_data(**kwargs)
        context['received_messages'] = Message.objects.filter(receiver=self.request.user, was_read=False)
        return context




@csrf_exempt
@login_required
def bookmark(request):
    if request.method == 'POST':
        doc_id = request.POST.get('doctor_id')

        fav = Favourites(patient=request.user.patientprofile, doctor_id=doc_id)
        fav.save()
    
    return HttpResponseRedirect(reverse('my_mr:doctor_detail', kwargs={'pk': doc_id}))



@csrf_exempt
@login_required
def bookmarkDelete(request):
    if request.method == 'POST':
        doc_id = request.POST.get('doctor_id')

        fav = Favourites.objects.filter(patient=request.user.patientprofile, doctor_id=doc_id)
        fav.delete()

    return HttpResponseRedirect(reverse('my_mr:doctor_detail', kwargs={'pk': doc_id}))



class InboxList(generic.ListView):
    context_object_name = 'inbox_list'
    template_name = 'my_mr/messages.html'
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
    template_name = 'my_mr/messages.html'
    paginate_by = 15

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super(SentList, self).get_context_data(**kwargs)
        context['received_messages'] = Message.objects.filter(receiver=self.request.user, was_read=False)
        context['type'] = 'sent'
        return context