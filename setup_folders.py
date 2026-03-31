import os

# Danh sách các thư mục cần tạo
directories = [
    "core/templates/core",
    "courses/templates/courses",
    "users/templates/users",
    "instructor/templates/instructor",
    "templates",
    "static/css",
    "static/js",
    "static/images",
    "media/course_covers",
    "media/lesson_files"
]

# Danh sách các file cần tạo
files = [
    "core/templates/core/index.html",
    "courses/templates/courses/list.html",
    "courses/templates/courses/category_list.html",
    "courses/templates/courses/detail.html",
    "courses/templates/courses/learn.html",
    "users/templates/users/login.html",
    "users/templates/users/register.html",
    "users/templates/users/profile.html",
    "users/templates/users/my_courses.html",
    "instructor/templates/instructor/dashboard.html",
    "instructor/templates/instructor/course_manage.html",
    "templates/base.html",
    "static/css/output.css",
    "static/js/main.js"
]

# Thực thi tạo thư mục
for dir_path in directories:
    os.makedirs(dir_path, exist_ok=True)
    print(f"📁 Đã tạo thư mục: {dir_path}")

# Thực thi tạo file trống
for file_path in files:
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            # Tạo sẵn cấu trúc kế thừa base.html cho các file giao diện
            if file_path.endswith('.html') and 'base.html' not in file_path:
                f.write("{% extends 'base.html' %}\n\n{% block content %}\n\n{% endblock %}")
            elif 'base.html' in file_path:
                f.write("<!DOCTYPE html>\n<html lang='vi'>\n<head>\n    <meta charset='UTF-8'>\n    <title>E-Learning</title>\n</head>\n<body>\n    {% block content %}{% endblock %}\n</body>\n</html>")
        print(f"📄 Đã tạo file: {file_path}")

print("\n✅ Hoàn tất! Cấu trúc thư mục của bạn đã sẵn sàng.")