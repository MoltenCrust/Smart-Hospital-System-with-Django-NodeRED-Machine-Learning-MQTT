from django.urls import path
from . import views

app_name = 'SmartHospitalSystem'

urlpatterns = [
    path('', views.update_page, name='homepage')
]