from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class Organization(models.Model):
    """مدل سازمان - می‌تونی ۵ تا بسازی"""
    name = models.CharField(max_length=100, verbose_name="نام سازمان")
    slug = models.SlugField(unique=True, verbose_name="شناسه")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    
    class Meta:
        verbose_name = "سازمان"
        verbose_name_plural = "سازمان‌ها"
    
    def __str__(self):
        return self.name

class User(AbstractUser):
    """مدل کاربر سفارشی با نقش‌های مختلف"""
    
    ROLE_CHOICES = [
        ('starter', 'شروع‌کننده'),
        ('sales', 'مشاور فروش'),
        ('manager', 'منیجر'),
        ('leader', 'راهبر'),
        ('admin', 'مدیرکل'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name="نقش")
    organization = models.ForeignKey(
        Organization, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='members',
        verbose_name="سازمان"
    )
    phone_regex = RegexValidator(regex=r'^09[0-9]{9}$', message="شماره موبایل باید ۱۱ رقم و با ۰۹ شروع شود")
    phone = models.CharField(validators=[phone_regex], max_length=11, unique=True, verbose_name="شماره موبایل")
    guardian_phone = models.CharField(validators=[phone_regex], max_length=11, null=True, blank=True, verbose_name="شماره حامی")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="عکس پروفایل")
    
    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
    
    def __str__(self):
        return f"{self.get_full_name()} - {self.get_role_display()}"
    
    def is_manager_or_leader(self):
        """بررسی آیا کاربر منیجر یا راهبر است"""
        return self.role in ['manager', 'leader']
