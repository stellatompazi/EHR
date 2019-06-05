from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import generic
from mr.models import *
from django.contrib.auth.decorators import login_required



# Create your views here.
def index(request):
    return render(request, 'my_mr/my_index.html', {'nbar': 'home'})



class DetailView(generic.DetailView):
    model = User
    template_name = 'my_mr/detail.html'

    def get_context_data(self, **kwargs):
        context = {"myprof": "active"}
        return context

class DetailUpdate(generic.UpdateView):
    model = PatientProfile
    fields = ['birthday', 'social_security_number', 'sex', 'insurance', 'blood', 'city', 'address', 'phone']
    template_name = "my_mr/detailsUpdate.html"

    def get_success_url(self):
        return reverse('my_mr:detail', kwargs={'pk': self.object.id})



class UserUpdate(generic.UpdateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']
    template_name = "my_mr/userUpdate.html"

    def get_success_url(self):
        return reverse('my_mr:detail', kwargs={'pk': self.object.id})



class appointments_list(generic.ListView):
    context_object_name = 'appointments_list'
    template_name = 'my_mr/appointments_list.html'
    paginate_by = 15

    def get_queryset(self):
        return Appointments.objects.filter(patient__user__username=self.request.user.username).order_by('-date')
    


class app_detail(generic.DetailView):
    model = Appointments
    template_name = 'my_mr/app_detail.html'

    def get_context_data(self, **kwargs):
        context = super(app_detail, self).get_context_data(**kwargs)
        context['icd10_list'] = App_icd10.objects.filter(appointment__id=self.kwargs['pk'])
        return context



class vaccinations_list(generic.ListView):
    context_object_name = 'vaccinations_list'
    template_name = 'my_mr/vaccinations_list.html'
    paginate_by = 15

    def get_queryset(self):
        return Vaccination.objects.filter(patient__user__username=self.request.user.username)
        


class vaccination_detail(generic.DetailView):
    model = Vaccination
    template_name = 'my_mr/vaccination_detail.html'



class surgeries_list(generic.ListView):
    context_object_name = 'surgeries_list'
    template_name = 'my_mr/surgeries_list.html'
    paginate_by = 15

    def get_queryset(self):
        return Surgery.objects.filter(patient__user__username=self.request.user.username)
        


class surgery_detail(generic.DetailView):
    model = Surgery
    template_name = 'my_mr/surgery_detail.html'


def specialties(request):
    return render(request, 'my_mr/specialties.html',
                            {'specialties': UserProfile.specialties_list})


class doctor_list(generic.ListView):
    context_object_name = 'doctor_list'
    template_name = 'my_mr/doctor_list.html'
    paginate_by = 15

    def get_queryset(self, *args, **kwargs):
        q = self.kwargs['slug']
        qnew = q.replace("_", " ")
        return UserProfile.objects.filter(specialty=qnew)


class doctor_detail(generic.DetailView):
    model = UserProfile
    template_name = 'my_mr/doctor_detail.html'

    def get_context_data(self, **kwargs):
        context = super(doctor_detail, self).get_context_data(**kwargs)
        context['price_list'] = Prices.objects.filter(doctor__id=self.kwargs['pk'])
        context['opening_hours_list'] = OpeningHours.objects.filter(doctor__id=self.kwargs['pk'])
        return context

