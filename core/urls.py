from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('organizations/', views.organization_list, name='organization_list'),
    path('organizations/create/', views.organization_create, name='organization_create'),
]
