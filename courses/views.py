from django.shortcuts import render, get_object_or_404 # Nhớ import thêm get_object_or_404
from .models import Course, Section, Lesson

def course_list(request):
    # Lấy toàn bộ khóa học từ Database
    # (Nếu Tài có cột trạng thái xuất bản, có thể dùng Course.objects.filter(is_published=True))
    courses = Course.objects.all()
    
    # Đóng gói dữ liệu vào biến 'courses' và gửi ra file HTML
    context = {
        'courses': courses
    }
    return render(request, 'courses/course_list.html', context)

def course_detail(request, slug):
    # 1. Tìm khóa học có slug khớp với URL, nếu không thấy thì báo lỗi 404
    course = get_object_or_404(Course, slug=slug)
    
    # 2. Lấy tất cả các Chương (Section) thuộc về khóa học này
    # Lưu ý: Mặc định Django tự tạo biến 'section_set' để móc nối dữ liệu con
    sections = course.sections.all().order_by('order')
    
    context = {
        'course': course,
        'sections': sections,
    }
    return render(request, 'courses/course_detail.html', context)

# TÌM HÀM NÀY VÀ SỬA LẠI THAM SỐ VÀ LỆNH GET:
def lesson_detail(request, course_slug, lesson_id): # <-- Sửa lesson_slug thành lesson_id
    course = get_object_or_404(Course, slug=course_slug)
    
    # Sửa lesson_slug=lesson_slug thành id=lesson_id
    lesson = get_object_or_404(Lesson, id=lesson_id, section__course=course) 
    
    sections = course.sections.all().order_by('order')
    
    context = {
        'course': course,
        'lesson': lesson,
        'sections': sections,
    }
    return render(request, 'courses/lesson_detail.html', context)