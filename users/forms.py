from django import forms
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model() # Dùng hàm này để lấy đúng model CustomUser của bạn

# 1. Form sửa thông tin cơ bản (Bỏ email)
class UserUpdateForm(forms.ModelForm):
    last_name = forms.CharField(label='Họ và tên đệm', max_length=100, required=False, 
        widget=forms.TextInput(attrs={'class': 'w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all'}))
    
    first_name = forms.CharField(label='Tên', max_length=100, required=False, 
        widget=forms.TextInput(attrs={'class': 'w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all'}))

    class Meta:
        model = User
        fields = ['last_name', 'first_name'] 
        # Đã xóa 'email' khỏi fields để không ai sửa được

# 2. Form sửa Hồ sơ (Profile)
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'phone', 'date_of_birth', 'gender', 'address', 'bio']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'w-full text-slate-400 file:mr-4 file:py-2.5 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-blue-500/20 file:text-blue-400 hover:file:bg-blue-500/30 transition-all cursor-pointer'}),
            'phone': forms.TextInput(attrs={'class': 'w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all', 'placeholder': 'VD: 0912345678'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all', 'style': 'color-scheme: dark;'}),
            'gender': forms.Select(attrs={'class': 'w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all'}),
            'address': forms.TextInput(attrs={'class': 'w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all'}),
            'bio': forms.Textarea(attrs={'class': 'w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all', 'rows': 4, 'placeholder': 'Vài dòng về bản thân bạn...'}),
        }
        labels = {
            'avatar': 'Ảnh đại diện',
            'phone': 'Số điện thoại',
            'date_of_birth': 'Ngày sinh',
            'gender': 'Giới tính',
            'address': 'Địa chỉ',
            'bio': 'Giới thiệu bản thân'
        }