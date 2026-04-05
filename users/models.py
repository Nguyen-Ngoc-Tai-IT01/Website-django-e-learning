from django.db import models
from django.contrib.auth.models import AbstractUser
from courses.models import LessonProgress
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

class CustomUser(AbstractUser):
    # Phân quyền cơ bản
    is_student = models.BooleanField(default=True)
    is_instructor = models.BooleanField(default=False)

    def __str__(self):
        return self.username

# BẢNG MỚI THÊM VÀO:
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    GENDER_CHOICES = (
        ('M', 'Nam'),
        ('F', 'Nữ'),
        ('O', 'Khác'),
    )
    # Đã thêm null=True vào đây để SQL Server không báo lỗi nữa
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
    
@login_required
def user_profile(request):
    # Lấy danh sách các bài học đã LƯU
    saved_lessons = LessonProgress.objects.filter(
        user=request.user, 
        is_saved=True
    ).select_related('lesson', 'lesson__course') # Dùng select_related để tối ưu truy vấn Database
    
    # Đếm số bài đã HOÀN THÀNH
    completed_count = LessonProgress.objects.filter(
        user=request.user, 
        is_completed=True
    ).count()

    context = {
        'saved_lessons': saved_lessons,
        'completed_count': completed_count,
    }
    return render(request, 'profile.html', context)