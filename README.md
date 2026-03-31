elearning_platform/
│
├── elearning_platform/             # Cấu hình project cốt lõi
│
├── core/                           # 👈 [MỚI] App xử lý Trang chủ
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       └── core/
│           └── index.html          # (STT 1) Trang chủ (Homepage)
│
├── courses/                        # App hiển thị Khóa học cho Học viên
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       └── courses/
│           ├── list.html           # (STT 2) Danh sách tất cả khóa học
│           ├── category_list.html  # 👈 [MỚI] (STT 3) Khóa học theo danh mục
│           ├── detail.html         # (STT 4) Chi tiết khóa học
│           └── learn.html          # 👈 [MỚI] (STT 5) Trang học chính (Video)
│
├── users/                          # App quản lý Người dùng
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       └── users/
│           ├── login.html          # (STT 8) Đăng nhập
│           ├── register.html       # (STT 9) Đăng ký
│           ├── profile.html        # 👈 [MỚI] (STT 7) Trang cá nhân
│           └── my_courses.html     # 👈 [MỚI] (STT 6) Khóa học của tôi
│
├── instructor/                     # 👈 [MỚI] App dành riêng cho Giảng viên
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       └── instructor/
│           ├── dashboard.html      # (STT 10) Dashboard giảng viên
│           └── course_manage.html  # (STT 11) Quản lý khóa học của giảng viên
│
├── templates/                      # Giao diện DÙNG CHUNG (Global)
│   ├── base.html                   # Layout gốc chứa Header, Footer
│   └── ...
│
├── static/                         # Tài nguyên tĩnh (CSS, JS)
├── media/                          # File upload (Ảnh bìa, Video)
└── manage.py