from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # STT 2: /courses/
    path('courses/', views.course_list, name='course_list'),
    
    # STT 3: /categories/<slug>/
    path('categories/<slug:category_slug>/', views.category_detail, name='category_detail'),
    
    # STT 4: /courses/<slug>/
    path('courses/<slug:course_slug>/', views.course_detail, name='course_detail'),
    
    # STT 5: /courses/<slug>/learn/
    path('courses/<slug:course_slug>/learn/', views.course_learn, name='course_learn'),
]