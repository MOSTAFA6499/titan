from django.db import models
from django.conf import settings
from django.core.validators import ValidationError
from datetime import date

class Attendance(models.Model):
    """مدل حضور و غیاب"""
    
    STATUS_CHOICES = [
        ('present', 'حاضر'),
        ('absent', 'غایب'),
        ('late', 'تأخیر'),
        ('excused', 'موجه'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="کاربر")
    course = models.ForeignKey('classes.Course', on_delete=models.CASCADE, null=True, blank=True, verbose_name="دوره")
    date = models.DateField(default=date.today, verbose_name="تاریخ")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name="وضعیت")
    marked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='marked_attendances', verbose_name="ثبت کننده")
    notes = models.TextField(blank=True, verbose_name="توضیحات")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'course', 'date']
        ordering = ['-date']
        verbose_name = "حضور و غیاب"
        verbose_name_plural = "حضور و غیاب‌ها"
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_status_display()} - {self.date}"
    
    def clean(self):
        """اعتبارسنجی: فقط منیجر یا راهبر می‌تونن ثبت کنن"""
        if self.marked_by and self.marked_by.role not in ['manager', 'leader']:
            raise ValidationError('فقط منیجر و راهبر می‌توانند حضور و غیاب ثبت کنند')
