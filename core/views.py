from django.shortcuts import render

def home(request):
    # Nếu người dùng ĐÃ ĐĂNG NHẬP
    if request.user.is_authenticated:
        # Nhảy vào trang xịn xò Tài vừa code xong
        return render(request, 'core/home.html') 
    
    # Nếu CHƯA ĐĂNG NHẬP (Khách vãng lai)
    else:
        # Nhảy vào trang giới thiệu (Tài tự tạo thêm 1 file intro.html nhé)
        return render(request, 'core/index.html')