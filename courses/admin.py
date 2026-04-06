from django.contrib import admin
from .models import Category, Course, Section, Lesson, CourseEnrollment, Document

# 1. Đăng ký các bảng đơn giản
admin.site.register(Category)
admin.site.register(Section)
admin.site.register(Lesson)
admin.site.register(CourseEnrollment)

# 2. Cấu hình bảng Course (QUAN TRỌNG: Nơi phân quyền giảng viên)
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'order', 'is_published')
    list_editable = ('order', 'is_published')
    # Loại bỏ instructor khỏi form nhập để nó tự động gán ở hàm save_model
    exclude = ('instructor',) 

    # Chỉ hiển thị khóa học của chính giảng viên đó
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Admin tổng thấy hết
        return qs.filter(instructor=request.user)

    # Tự động gán giảng viên đang đăng nhập vào khóa học khi bấm Save
    def save_model(self, request, obj, form, change):
        if not obj.pk: # Nếu là tạo mới
            obj.instructor = request.user
        super().save_model(request, obj, form, change)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    search_fields = ('title',)
    
