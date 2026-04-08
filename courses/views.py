from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Section, Lesson, LessonProgress, Document, Category, CourseEnrollment
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Prefetch
from django.contrib import messages

def course_list(request):
    # Lấy từ khóa người dùng gõ vào ô tìm kiếm (biến 'q')
    query = request.GET.get('q')
    
    if query:
        # Nếu có gõ tìm kiếm: Lọc khóa học có chứa từ khóa trong Tiêu đề HOẶC Mô tả
        # icontains: tìm kiếm không phân biệt chữ hoa/thường
        courses = Course.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    else:
        # Nếu không tìm kiếm gì: Hiển thị toàn bộ khóa học như cũ
        courses = Course.objects.all()
    
    context = {
        'courses': courses,
        'query': query, # Truyền từ khóa ra giao diện để hiển thị
    }
    return render(request, 'courses/course_list.html', context)

def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    sections = course.sections.all()
    
    # Kiểm tra xem User đã đăng ký khóa này chưa
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = CourseEnrollment.objects.filter(user=request.user, course=course).exists()
        
    return render(request, 'courses/course_detail.html', {
        'course': course, 
        'sections': sections,
        'is_enrolled': is_enrolled # Ném biến này ra HTML
    })

# 2. Thêm hàm xử lý khi người dùng bấm nút "Đăng ký"
@login_required
def enroll_course(request, slug):
    if request.method == 'POST':
        course = get_object_or_404(Course, slug=slug)
        # get_or_create giúp tạo bản ghi mới, nếu họ bấm 2 lần thì cũng không bị lỗi tạo trùng
        CourseEnrollment.objects.get_or_create(user=request.user, course=course)
        
        messages.success(request, f"Chúc mừng bạn đã đăng ký thành công khóa học: {course.title}!")
        
    # Xong việc thì load lại trang chi tiết khóa học đó
    return redirect('courses:course_detail', slug=slug)
# TÌM HÀM NÀY VÀ SỬA LẠI THAM SỐ VÀ LỆNH GET:
def lesson_detail(request, course_slug, lesson_id):
    # Lấy thông tin bài học và khóa học
    course = get_object_or_404(Course, slug=course_slug)
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
	# hiển thị danh sách các bài học 
    sections = course.sections.all()     
    # xử lý tiến độ 
    user_progress = None
    if request.user.is_authenticated:
        user_progress = LessonProgress.objects.filter(user=request.user, lesson=lesson).first()

    context = {
        'course': course,
        'lesson': lesson,
        'sections': sections,       
        'user_progress': user_progress,
    }
    return render(request, 'courses/lesson_detail.html', context)


# xử lý logic lưu bài và hoàn thành bài 
@login_required
@require_POST
def toggle_progress(request, lesson_id):
    action_type = request.POST.get('type') # 'complete' hoặc 'save'
    progress, created = LessonProgress.objects.get_or_create(
        user=request.user, 
        lesson_id=lesson_id
    )
    
    if action_type == 'complete':
        progress.is_completed = not progress.is_completed
    elif action_type == 'save':
        progress.is_saved = not progress.is_saved
        
    progress.save()
    return JsonResponse({
        'status': 'success',
        'is_completed': progress.is_completed,
        'is_saved': progress.is_saved
    })
    
# 1. Hàm hiển thị danh sách toàn bộ sách (Trang Thư viện)
def document_list(request):
    documents = Document.objects.all()
    return render(request, 'courses/document_list.html', {'documents': documents})

# # 2. Hàm hiển thị chi tiết 1 cuốn sách để đọc (Trang Đọc sách)
# def document_detail(request, doc_id):
#     document = get_object_or_404(Document, id=doc_id)
    
#     is_pdf = False
#     if document.file:
#         ext = document.file.name.split('.')[-1].lower()
#         is_pdf = ext == 'pdf'
    
#     return render(request, 'courses/document_detail.html', {
#         'document': document,
#         'is_pdf': is_pdf,          
#     })

def roadmap(request):
    # Lấy tất cả Danh mục, và ÉP các khóa học bên trong phải được sắp xếp chuẩn theo cột 'order' (từ nhỏ đến lớn)
    categories = Category.objects.prefetch_related(
        Prefetch('courses', queryset=Course.objects.order_by('order'))
    ).all()
    
    return render(request, 'courses/roadmap.html', {'categories': categories})