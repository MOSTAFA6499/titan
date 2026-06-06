from django import forms
from .models import Course, Lesson, ClassLevel

class CourseForm(forms.ModelForm):
    """فرم ایجاد و ویرایش دوره"""
    
    class Meta:
        model = Course
        fields = ('title', 'description', 'required_level', 'image', 'is_active')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

class LessonForm(forms.ModelForm):
    """فرم ایجاد جلسه جدید"""
    
    class Meta:
        model = Lesson
        fields = ('title', 'content_type', 'content_url', 'content_file', 'order', 'duration')
