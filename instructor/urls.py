from django.urls import path
from . import views

app_name = 'instructor'

urlpatterns = [
    # STT 10: /instructor/dashboard/
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # STT 11: /instructor/courses/
    path('courses/', views.manage_courses, name='manage_courses'),
]