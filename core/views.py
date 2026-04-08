from django.shortcuts import render
from courses.models import Course

def home(request):
    # 1. Bốc ngẫu nhiên 3 khóa học (Chuẩn bị sẵn dữ liệu)
    random_courses = Course.objects.filter(is_published=True).order_by('?')[:3]
    
    # 2. Đóng gói dữ liệu vào một biến context
    context = {
        'random_courses': random_courses
    }

    # 3. Kiểm tra xem người dùng là ai để điều hướng
    if request.user.is_authenticated:
        # Nếu ĐÃ ĐĂNG NHẬP: Vào trang Dashboard/Home và mang theo 3 khóa học
        return render(request, 'core/home.html', context) 
    
    else:
        # Nếu CHƯA ĐĂNG NHẬP: Vào trang Landing Page/Index và cũng mang theo 3 khóa học
        return render(request, 'core/index.html', context)