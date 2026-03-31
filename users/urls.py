from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # STT 8: /accounts/login/
    path('accounts/login/', views.user_login, name='login'),
    
    # STT 9: /accounts/register/
    path('accounts/register/', views.user_register, name='register'),
    
    # STT 7: /profile/
    path('profile/', views.user_profile, name='profile'),
    
    # STT 6: /my-courses/
    path('my-courses/', views.my_courses, name='my_courses'),
]