from django.urls import path
from userMessages import views


app_name = 'userMessages'
urlpatterns = [
    path('messageForm/', views.MessageForm, name='message_form'),
    path('message/read/', views.MessageRead, name='mark_read')
]