from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # Các URL cố định phải đặt lên TRÊN CÙNG
    path('', views.course_list, name='course_list'),
    path('tai-lieu/', views.document_list, name='document_list'), 
    path('lo-trinh/', views.roadmap, name='roadmap'),
	# path('tai-lieu/<int:doc_id>/', views.document_detail, name='document_detail'),
    # Các URL có chứa biến (như <slug:...> hay <int:...>) phải đặt XUỐNG DƯỚI
    path('<slug:slug>/enroll/', views.enroll_course, name='enroll_course'),
    path('<slug:slug>/', views.course_detail, name='course_detail'), 
    path('lesson/<int:lesson_id>/toggle-progress/', views.toggle_progress, name='toggle_progress'),
    path('<slug:course_slug>/lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
]