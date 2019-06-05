from django.urls import path
from . import views

app_name = 'mr'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('update/<int:pk>/', views.DetailUpdate.as_view(), name='update_profile_detail'),
    path('updateUser/<int:pk>/', views.UserUpdate.as_view(), name='update_user'),
    path('register_patient/', views.register_patient, name='register_patient'),
    path('search_results/', views.search_results, name='search_results'),
    path('patient_details/<int:pk>/', views.patient_details.as_view(), name='patient_details'),
    path('patient_details/add_appointment/', views.add_appointment, name='add_appointment'),
    path('patient_details/add_appointment/icd10', views.add_icd10_codes, name='add_icd10_codes'),
    path('patient_details/appointment/delete/<int:pk>/', views.AppointmentDelete.as_view(), name='delete_appointment'),
    path('patient_details/appointment/edit/<int:pk>/', views.AppointmentUpdate.as_view(), name='update_appointment'),
    path('patient_details/add_vaccination/', views.add_vaccination, name='add_vaccination'),
    path('patient_details/add_surgery/', views.add_surgery, name='add_surgery'),
    path('patient_details/add_exam_file/', views.add_exam_file, name='add_exam_file'),
    path('patient_details/appointments_list/', views.appointments_list.as_view(), name='appointments_list'),
    path('patient_details/appointments_detail/<int:pk>/', views.appointments_detail.as_view(), name='appointments_detail'),
    path('patient_details/vaccinations_list/', views.vaccinations_list.as_view(), name='vaccinations_list'),
    path('patient_details/vaccination_detail/<int:pk>/', views.vaccination_detail.as_view(), name='vaccination_detail'),
    path('patient_details/surgeries_list/', views.surgeries_list.as_view(), name='surgeries_list'),
    path('patient_details/surgery_detail/<int:pk>/', views.surgery_detail.as_view(), name='surgery_detail'),
    path('pricelist/', views.price_list.as_view(), name='price_list'),
    path('add_price/', views.add_price, name='add_price'),
    path('opening_hours/', views.opening_hours.as_view(), name='opening_hours'),
    path('opening_hours/add/', views.add_opening_hours, name='add_opening_hours'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('calendar/new_event/', views.new_event, name='new_event'),
    path('calendar/event/edit/<int:pk>/', views.EventUpdate.as_view(), name='edit_event')
]