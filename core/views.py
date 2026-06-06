from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Organization, User
from .forms import OrganizationForm, UserProfileForm

@login_required
def dashboard(request):
    """داشبورد اصلی بر اساس نقش کاربر"""
    user = request.user
    context = {
        'user': user,
    }
    
    if user.role == 'leader':
        # پنل راهبر - آمار کل سازمان‌ها
        context['total_organizations'] = Organization.objects.count()
        context['total_users'] = User.objects.count()
        context['recent_users'] = User.objects.order_by('-date_joined')[:10]
        template = 'dashboard/leader_dashboard.html'
    
    elif user.role == 'manager':
        # پنل منیجر - مدیریت کاربران و کلاس‌های سازمان خودش
        context['users'] = User.objects.filter(organization=user.organization)
        template = 'dashboard/manager_dashboard.html'
    
    elif user.role == 'sales':
        # پنل مشاور فروش - پیگیری افراد تحت پوشش
        context['assigned_users'] = []  # بعداً تکمیل می‌شه
        template = 'dashboard/sales_dashboard.html'
    
    else:  # starter
        # پنل شروع‌کننده - دوره‌های من
        template = 'dashboard/starter_dashboard.html'
    
    return render(request, template, context)

@login_required
def profile(request):
    """پروفایل کاربر"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'پروفایل با موفقیت به‌روز شد')
            return redirect('core:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'core/profile.html', {'form': form})

@login_required
def organization_list(request):
    """لیست سازمان‌ها (فقط برای راهبر)"""
    if request.user.role != 'leader':
        messages.error(request, 'شما دسترسی به این صفحه ندارید')
        return redirect('core:dashboard')
    
    organizations = Organization.objects.all()
    return render(request, 'core/organization_list.html', {'organizations': organizations})

@login_required
def organization_create(request):
    """ساخت سازمان جدید (فقط برای راهبر)"""
    if request.user.role != 'leader':
        messages.error(request, 'شما دسترسی به این صفحه ندارید')
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'سازمان با موفقیت ساخته شد')
            return redirect('core:organization_list')
    else:
        form = OrganizationForm()
    
    return render(request, 'core/organization_form.html', {'form': form})
