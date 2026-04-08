from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
import re
from django.contrib.auth.decorators import login_required
from courses.models import LessonProgress, CourseEnrollment
from .models import Profile
from .forms import UserUpdateForm
from .forms import UserUpdateForm, ProfileUpdateForm

# Gọi model CustomUser mà Tài đã tạo hôm trước
User = get_user_model()

def user_register(request):
    regex = '^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$'
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        old_data = {
            'old_username': username,
            'old_email': email,
        }

        if password != confirm_password:
            messages.error(request, 'Mật khẩu xác nhận không khớp!')
            return render(request, 'users/register.html', old_data)
        
        if not re.match(regex, password):
            messages.error(request, 'Mật khẩu không đủ mạnh! Cần ít nhất 6 ký tự, bao gồm cả chữ và số.')
            return render(request, 'users/register.html', old_data)
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Tên đăng nhập đã có người sử dụng!')
            return render(request, 'users/register.html', old_data)

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        messages.success(request, 'Đăng ký thành công! Vui lòng đăng nhập.')
        return redirect('users:login')

    return render(request, 'users/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        old_data = {
			'old_username': username
		}

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect( 'core:home')
        else:
            messages.error(request, 'Sai tên đăng nhập hoặc mật khẩu!')
            return render(request, 'users/login.html', old_data)

    return render(request, 'users/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'Bạn đã đăng xuất thành công. Hẹn gặp lại!')
    return redirect('core:home')	

@login_required
def user_profile(request):
    # 1. Khắc phục triệt để lỗi "User has no profile" lúc trước
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    # 2. THÊM MỚI: Lấy danh sách các khóa học mà user này đã bấm "Đăng ký"
    enrolled_courses = CourseEnrollment.objects.filter(
        user=request.user
    ).select_related('course')

    # 3. GIỮ NGUYÊN: Lôi dữ liệu 1 đường thẳng từ Lesson -> Section -> Course
    saved_lessons = LessonProgress.objects.filter(
        user=request.user, 
        is_saved=True
    ).select_related('lesson__section__course') 
    
    # 4. GIỮ NGUYÊN: Đếm số bài giảng đã hoàn thành
    completed_count = LessonProgress.objects.filter(
        user=request.user, 
        is_completed=True
    ).count()

    # Đóng gói tất cả bỏ vào context gửi ra giao diện
    context = {
        'saved_lessons': saved_lessons,
        'completed_count': completed_count,
        'enrolled_courses': enrolled_courses, # <--- Nhớ có dòng này để mang ra HTML
    }
    return render(request, 'users/profile.html', context)	

@login_required
def apply_instructor(request):
    # Dùng get_or_create thay cho request.user.profile
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if not request.user.is_staff:
        profile.is_instructor_pending = True
        profile.save()
        messages.success(request, "Yêu cầu làm giảng viên đã được gửi! Đợi Admin duyệt nhé.")
        
    return redirect('users:profile')

@login_required
def edit_profile(request):
    # Đảm bảo user có profile
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # Bắt buộc thêm request.FILES để nhận ảnh
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile) 
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Hồ sơ của bạn đã được cập nhật thành công!')
            return redirect('users:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/edit_profile.html', context)