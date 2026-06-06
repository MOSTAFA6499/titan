from django.urls import path
from . import views

app_name = 'classes'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('course/create/', views.course_create, name='course_create'),
    path('lesson/create/<int:course_id>/', views.lesson_create, name='lesson_create'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
]
