from django.db import models
from django.conf import settings

class ClassLevel(models.Model):
    """سطوح کلاس‌بندی - ۵ سطح اصلی سیستم"""
    
    LEVEL_CHOICES = [
        ('starter', 'شروع‌کننده'),
        ('sales', 'مشاور فروش'),
        ('management', 'منجمنت'),
        ('pre_leadership', 'Pre Leadership'),
        ('leadership', 'Leadership'),
    ]
    
    name = models.CharField(max_length=50, choices=LEVEL_CHOICES, unique=True, verbose_name="نام سطح")
    order = models.IntegerField(default=0, verbose_name="ترتیب")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    
    class Meta:
        ordering = ['order']
        verbose_name = "سطح کلاس"
        verbose_name_plural = "سطوح کلاس‌ها"
    
    def __str__(self):
        return self.get_name_display()

class Course(models.Model):
    """مدل دوره‌های آموزشی"""
    
    title = models.CharField(max_length=200, verbose_name="عنوان دوره")
    description = models.TextField(verbose_name="توضیحات")
    required_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, verbose_name="سطح مورد نیاز")
    organization = models.ForeignKey('core.Organization', on_delete=models.CASCADE, verbose_name="سازمان")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="ایجاد کننده")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    image = models.ImageField(upload_to='courses/', blank=True, null=True, verbose_name="تصویر دوره")
    
    class Meta:
        verbose_name = "دوره"
        verbose_name_plural = "دوره‌ها"
    
    def __str__(self):
        return self.title

class Lesson(models.Model):
    """مدل محتواهای هر دوره"""
    
    CONTENT_TYPES = [
        ('video', 'ویدیو'),
        ('document', 'مستند'),
        ('quiz', 'آزمون'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name="دوره")
    title = models.CharField(max_length=200, verbose_name="عنوان جلسه")
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES, verbose_name="نوع محتوا")
    content_url = models.URLField(blank=True, null=True, verbose_name="لینک محتوا")
    content_file = models.FileField(upload_to='lesson_contents/', blank=True, null=True, verbose_name="فایل محتوا")
    order = models.IntegerField(default=0, verbose_name="ترتیب")
    duration = models.IntegerField(default=0, help_text="مدت زمان به دقیقه", verbose_name="مدت زمان")
    
    class Meta:
        ordering = ['order']
        verbose_name = "جلسه"
        verbose_name_plural = "جلسات"
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Enrollment(models.Model):
    """ثبت‌نام افراد در دوره‌ها"""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="کاربر")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="دوره")
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False, verbose_name="تکمیل شده")
    completed_at = models.DateTimeField(null=True, blank=True)
    progress = models.IntegerField(default=0, verbose_name="درصد پیشرفت")
    
    class Meta:
        unique_together = ['user', 'course']
        verbose_name = "ثبت‌نام"
        verbose_name_plural = "ثبت‌نام‌ها"
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.course.title}"
