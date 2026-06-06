from django import forms
from .models import Attendance

class AttendanceForm(forms.ModelForm):
    """فرم ثبت حضور و غیاب"""
    
    class Meta:
        model = Attendance
        fields = ('user', 'course', 'status', 'notes')
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
