from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import Course, Lesson, Enrollment, ClassLevel
from .forms import CourseForm, LessonForm

def is_manager_or_leader(user):
    """بررسی اینکه کاربر منیجر یا راهبر باشد"""
    return user.role in ['manager', 'leader']

@login_required
def course_list(request):
    """لیست دوره‌ها"""
    courses = Course.objects.filter(is_active=True)
    
    # فیلتر بر اساس سازمان کاربر
    if request.user.organization:
        courses = courses.filter(organization=request.user.organization)
    
    return render(request, 'classes/course_list.html', {'courses': courses})

@login_required
def course_detail(request, pk):
    """جزئیات دوره و جلسات آن"""
    course = get_object_or_404(Course, pk=pk)
    lessons = course.lessons.all()
    
    # بررسی اینکه کاربر در این دوره ثبت‌نام کرده یا نه
    is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()
    
    return render(request, 'classes/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'is_enrolled': is_enrolled,
    })

@login_required
@user_passes_test(is_manager_or_leader)
def course_create(request):
    """ایجاد دوره جدید (فقط منیجر و راهبر)"""
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.created_by = request.user
            course.organization = request.user.organization
            course.save()
            messages.success(request, 'دوره با موفقیت ساخته شد')
            return redirect('classes:course_detail', pk=course.pk)
    else:
        form = CourseForm()
    
    return render(request, 'classes/course_form.html', {'form': form})

@login_required
@user_passes_test(is_manager_or_leader)
def lesson_create(request, course_id):
    """ایجاد جلسه جدید برای دوره (فقط منیجر و راهبر)"""
    course = get_object_or_404(Course, pk=course_id)
    
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            messages.success(request, 'جلسه با موفقیت اضافه شد')
            return redirect('classes:course_detail', pk=course.pk)
    else:
        form = LessonForm()
    
    return render(request, 'classes/lesson_form.html', {'form': form, 'course': course})

@login_required
def enroll_course(request, course_id):
    """ثبت‌نام کاربر در دوره"""
    course = get_object_or_404(Course, pk=course_id)
    
    # بررسی سطح دسترسی
    if request.user.role == 'starter':
        # بررسی سطح مورد نیاز
        user_level = ClassLevel.objects.filter(name=request.user.role).first()
        if user_level and user_level.order < course.required_level.order:
            messages.error(request, 'برای ثبت‌نام در این دوره باید سطح بالاتری داشته باشی')
            return redirect('classes:course_detail', pk=course.pk)
    
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user,
        course=course
    )
    
    if created:
        messages.success(request, f'شما در دوره {course.title} ثبت‌نام شدی')
    else:
        messages.info(request, 'شما قبلاً در این دوره ثبت‌نام کرده‌ای')
    
    return redirect('classes:course_detail', pk=course.pk)
