from django.contrib import admin
from .models import Category, Course, Section, Lesson, CourseEnrollment

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Lesson)
admin.site.register(CourseEnrollment)