from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
import re

# Gọi model CustomUser mà Tài đã tạo hôm trước
User = get_user_model()

def user_register(request):
    regex = '^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$'
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Gom các thông tin đã nhập (trừ mật khẩu) để gửi trả lại giao diện
        old_data = {
            'old_username': username,
            'old_email': email,
        }

        # Kiểm tra mật khẩu có khớp không
        if password != confirm_password:
            messages.error(request, 'Mật khẩu xác nhận không khớp!')
            return render(request, 'users/register.html', old_data)
        
        # Check mật khẩu có mạnh không
        if not re.match(regex, password):
            messages.error(request, 'Mật khẩu không đủ mạnh! Cần ít nhất 6 ký tự, bao gồm cả chữ và số.')
            return render(request, 'users/register.html', old_data)
        
        # Kiểm tra xem user đã tồn tại chưa
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Tên đăng nhập đã có người sử dụng!')
            return render(request, 'users/register.html', old_data)

        # Lưu vào Database SQL Server
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        # Thành công quay về trang đăng nhập
        messages.success(request, 'Đăng ký thành công! Vui lòng đăng nhập.')
        return redirect('users:login')

    # nếu người dùng chỉ mới truy cập vào trang 
    return render(request, 'users/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        old_data = {
			'old_username': username
		}

        # Kiểm tra thông tin đăng nhập
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Đăng nhập thành công, chuyển hướng về Trang chủ
            login(request, user)
            return redirect( 'core:home')
        else:
            # Đăng nhập thất bại
            messages.error(request, 'Sai tên đăng nhập hoặc mật khẩu!')
            return render(request, 'users/login.html', old_data)

    return render(request, 'users/login.html')

def user_logout(request):
    # Lệnh này sẽ xóa session và đăng xuất người dùng hiện tại
    logout(request)
    
    # Báo thông báo thành công
    messages.success(request, 'Bạn đã đăng xuất thành công. Hẹn gặp lại!')
    
    # Đăng xuất xong thì đá về lại trang chủ (lúc này sẽ là trang intro vì không còn đăng nhập nữa)
    return redirect('core:home')	