from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('attendance/', views.attendance_report_export, name='attendance_report'),
    path('progress/<int:user_id>/', views.student_progress_report, name='student_progress'),
]
