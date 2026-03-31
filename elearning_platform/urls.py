from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Kết nối tới App 'core' (Trang chủ)
    path('', include('core.urls', namespace='core')),
    
    # Kết nối tới App 'courses' (Hiển thị khóa học)
    path('', include('courses.urls', namespace='courses')),
    
    # Kết nối tới App 'users' (Tài khoản & Cá nhân)
    path('', include('users.urls', namespace='users')),
    
    # Kết nối tới App 'instructor' (Khu vực giảng viên)
    # Tiền tố 'instructor/' được đặt ở đây, các URL con sẽ tự động nối vào sau
    path('instructor/', include('instructor.urls', namespace='instructor')),
]