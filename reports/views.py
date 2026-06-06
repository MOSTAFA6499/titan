import pandas as pd
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from attendance.models import Attendance
from core.models import User
from classes.models import Enrollment, Course

@login_required
def attendance_report_export(request):
    """گزارش حضور و غیاب به صورت اکسل"""
    
    user_id = request.GET.get('user_id')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    
    attendances = Attendance.objects.all()
    
    if request.user.role == 'manager' and request.user.organization:
        attendances = attendances.filter(user__organization=request.user.organization)
    elif request.user.role == 'sales':
        # مشاور فروش فقط افراد خودش رو ببینه
        pass
    
    if user_id:
        attendances = attendances.filter(user_id=user_id)
    if from_date:
        attendances = attendances.filter(date__gte=from_date)
    if to_date:
        attendances = attendances.filter(date__lte=to_date)
    
    # تبدیل به دیتافریم پانداس
    data = []
    for att in attendances:
        data.append({
            'نام کاربر': att.user.get_full_name(),
            'تاریخ': att.date,
            'وضعیت': att.get_status_display(),
            'ثبت کننده': att.marked_by.get_full_name(),
            'توضیحات': att.notes,
        })
    
    df = pd.DataFrame(data)
    
    # ساخت پاسخ اکسل
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="attendance_report.xlsx"'
    
    df.to_excel(response, index=False, engine='openpyxl')
    
    return response

@login_required
def student_progress_report(request, user_id):
    """گزارش پیشرفت یک دانش‌آموز"""
    
    if request.user.role not in ['manager', 'leader'] and request.user.id != user_id:
        messages.error(request, 'شما دسترسی به این گزارش ندارید')
        return redirect('core:dashboard')
    
    student = User.objects.get(id=user_id)
    enrollments = Enrollment.objects.filter(user=student)
    
    data = []
    for enrollment in enrollments:
        data.append({
            'دوره': enrollment.course.title,
            'وضعیت': 'تکمیل شده' if enrollment.completed else 'در حال پیشرفت',
            'درصد پیشرفت': enrollment.progress,
            'تاریخ ثبت‌نام': enrollment.enrolled_at,
        })
    
    df = pd.DataFrame(data)
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="progress_{student.username}.xlsx"'
    
    df.to_excel(response, index=False, engine='openpyxl')
    
    return response
