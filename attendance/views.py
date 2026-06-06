from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import Attendance
from core.models import User
from classes.models import Course

def is_manager_or_leader(user):
    return user.role in ['manager', 'leader']

@login_required
def attendance_list(request):
    """لیست حضور و غیاب‌ها"""
    attendances = Attendance.objects.all()
    
    # فیلتر بر اساس سازمان کاربر
    if request.user.organization:
        attendances = attendances.filter(user__organization=request.user.organization)
    
    return render(request, 'attendance/attendance_list.html', {'attendances': attendances})

@login_required
@user_passes_test(is_manager_or_leader)
def mark_attendance(request):
    """ثبت حضور و غیاب (فقط منیجر و راهبر)"""
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        course_id = request.POST.get('course_id')
        status = request.POST.get('status')
        
        user = get_object_or_404(User, id=user_id)
        course = get_object_or_404(Course, id=course_id) if course_id else None
        
        attendance, created = Attendance.objects.update_or_create(
            user=user,
            course=course,
            date=timezone.now().date(),
            defaults={
                'status': status,
                'marked_by': request.user,
            }
        )
        
        messages.success(request, f'حضور و غیاب {user.get_full_name()} ثبت شد')
        
        # اگر غیبت بود و شماره حامی داشت، پیامک بفرست
        if status == 'absent' and user.guardian_phone:
            # پیاده‌سازی ارسال پیامک بعداً اضافه می‌شه
            pass
        
        return redirect('attendance:attendance_list')
    
    users = User.objects.filter(organization=request.user.organization, role='starter')
    courses = Course.objects.filter(organization=request.user.organization, is_active=True)
    
    return render(request, 'attendance/mark_attendance.html', {
        'users': users,
        'courses': courses,
    })

@login_required
def attendance_report(request):
    """گزارش حضور و غیاب"""
    user_id = request.GET.get('user_id')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    
    attendances = Attendance.objects.all()
    
    if user_id:
        attendances = attendances.filter(user_id=user_id)
    if from_date:
        attendances = attendances.filter(date__gte=from_date)
    if to_date:
        attendances = attendances.filter(date__lte=to_date)
    
    users = User.objects.filter(organization=request.user.organization, role='starter')
    
    return render(request, 'attendance/attendance_report.html', {
        'attendances': attendances,
        'users': users,
    })
