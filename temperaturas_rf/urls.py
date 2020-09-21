
from django.contrib import admin
from django.urls import path
from temperaturas_rf import views
from .views import index, fetchTemperatures

urlpatterns = [
    path('', index, name='index'),
    path('fetch', fetchTemperatures)
]
