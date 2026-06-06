from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Organization

class UserRegistrationForm(UserCreationForm):
    """فرم ثبت‌نام کاربر جدید"""
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone', 'role', 'organization', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-input'})

class UserProfileForm(forms.ModelForm):
    """فرم ویرایش پروفایل"""
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'guardian_phone', 'avatar')

class OrganizationForm(forms.ModelForm):
    """فرم ساخت و ویرایش سازمان"""
    
    class Meta:
        model = Organization
        fields = ('name', 'slug', 'is_active')
