from django.contrib import admin
from django.urls import path, include # Nhớ thêm chữ include ở đây
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # Dòng này nối thẳng trang chủ vào app core
    path('', include('core.urls', namespace='core')), 
    path('users/', include('users.urls', namespace='users')),
    path('courses/', include('courses.urls', namespace='courses'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)