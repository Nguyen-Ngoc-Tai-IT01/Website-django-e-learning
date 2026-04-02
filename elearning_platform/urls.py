from django.contrib import admin
from django.urls import path, include # Nhớ thêm chữ include ở đây

urlpatterns = [
    path('admin/', admin.site.urls),
    # Dòng này nối thẳng trang chủ vào app core
    path('', include('core.urls', namespace='core')), 
]