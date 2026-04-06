from django.shortcuts import render, get_object_or_404
from .models import Course, Section, Lesson, LessonProgress, Document, Category
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Prefetch

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