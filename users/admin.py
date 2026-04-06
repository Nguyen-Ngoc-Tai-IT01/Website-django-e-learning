from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Profile

# Định nghĩa hành động duyệt nhanh
@admin.action(description='Phê duyệt các giảng viên đã chọn')
def approve_as_instructor(modeladmin, request, queryset):
    try:
        group = Group.objects.get(name='Giảng viên')
        for profile in queryset:
            user = profile.user
            user.is_staff = True
            user.groups.add(group)
            user.save()
            
            profile.is_instructor_pending = False
            profile.save()
    except Group.DoesNotExist:
        # Nếu chưa tạo Group 'Giảng viên' trong Admin thì báo lỗi nhẹ
        from django.contrib import messages
        messages.error(request, "Lỗi: Bạn chưa tạo Group tên là 'Giảng viên' trong trang Admin!")

# Đăng ký Profile với class Admin tùy chỉnh
@admin.register(Profile) # <--- Chỉ dùng cái này để đăng ký, không dùng admin.site.register nữa
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_instructor_pending')
    list_filter = ('is_instructor_pending',)
    actions = [approve_as_instructor]