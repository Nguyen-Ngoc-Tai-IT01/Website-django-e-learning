from django.contrib import admin
from .models import Category, Course, Section, Lesson, CourseEnrollment, Document


admin.site.register(Category)
admin.site.register(CourseEnrollment)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    search_fields = ('title',)



@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'is_published', 'created_at')
    list_editable = ('is_published',)
    exclude = ('instructor',) 

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  
        return qs.filter(instructor=request.user)

    # Tự động gán giảng viên đang đăng nhập vào khóa học khi bấm Save
    def save_model(self, request, obj, form, change):
        if not getattr(obj, 'instructor_id', None):
            obj.instructor = request.user
        super().save_model(request, obj, form, change)

    # Chặn đứng việc sửa/xóa nếu cố tình truy cập ID của người khác
    def has_change_permission(self, request, obj=None):
        if not obj or request.user.is_superuser:
            return True
        return obj.instructor == request.user

    def has_delete_permission(self, request, obj=None):
        if not obj or request.user.is_superuser:
            return True
        return obj.instructor == request.user

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_editable = ('order',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Chỉ lấy các Chương thuộc Khóa học của giảng viên này
        return qs.filter(course__instructor=request.user)

    # Giới hạn dropdown: Giảng viên chỉ được chọn Khóa học của chính mình
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "course" and not request.user.is_superuser:
            kwargs["queryset"] = Course.objects.filter(instructor=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        if not obj or request.user.is_superuser:
            return True
        return obj.course.instructor == request.user

    def has_delete_permission(self, request, obj=None):
        if not obj or request.user.is_superuser:
            return True
        return obj.course.instructor == request.user


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'order')
    list_editable = ('order',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Chỉ lấy bài giảng thuộc Chương -> thuộc Khóa học của giảng viên này
        return qs.filter(section__course__instructor=request.user)

    # Giới hạn dropdown: Giảng viên chỉ được chọn Chương của chính mình
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "section" and not request.user.is_superuser:
            kwargs["queryset"] = Section.objects.filter(course__instructor=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        if not obj or request.user.is_superuser:
            return True
        return obj.section.course.instructor == request.user

    def has_delete_permission(self, request, obj=None):
        if not obj or request.user.is_superuser:
            return True
        return obj.section.course.instructor == request.user