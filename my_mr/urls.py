from django.urls import path
from my_mr import views

app_name = 'my_mr'
urlpatterns = [
    path('', views.index, name='my_index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('update/<int:pk>/', views.DetailUpdate.as_view(), name='update_profile_detail'),
    path('updateUser/<int:pk>/', views.UserUpdate.as_view(), name='update_user'),
    path('scheduled_appointment/<int:pk>/', views.ScheduledApp.as_view(), name='scheduled_app'),
    path('appointments_list/', views.appointments_list.as_view(), name='appointments_list'),
    path('app_detail/<int:pk>/', views.app_detail.as_view(), name='app_detail'),
    path('vaccinations_list/', views.vaccinations_list.as_view(), name='vaccinations_list'),
    path('vaccination_detail/<int:pk>/', views.vaccination_detail.as_view(), name='vaccination_detail'),
    path('surgeries_list/', views.surgeries_list.as_view(), name='surgeries_list'),
    path('surgery_detail/<int:pk>/', views.surgery_detail.as_view(), name='surgery_detail'),
    path('specialties/', views.specialties, name='specialties'),
    path('specialties/<slug:slug>/', views.doctor_list.as_view(), name='doctor_list'),
    path('doctor_detail/<int:pk>/', views.doctor_detail.as_view(), name='doctor_detail'),
    path('favourites/', views.FavouritesList.as_view(), name='favourites'),
    path('bookmark/add/', views.bookmark, name='bookmark'),
    path('bookmark/delete/', views.bookmarkDelete, name='bookmark_delete'),
    path('messages/inbox/', views.InboxList.as_view(), name='inbox'),
    path('messages/delete/<int:pk>/', views.MessageDelete.as_view(), name='delete_message'),
    path('messages/sent/', views.SentList.as_view(), name='sent')
]