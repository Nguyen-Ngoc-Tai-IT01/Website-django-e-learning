from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # STT 1: / (Homepage)
    path('', views.home, name='homepage'),
]