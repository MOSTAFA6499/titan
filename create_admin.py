import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'titan_config.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import Organization

User = get_user_model()

# اطلاعات ادمین تو - با همون یوزر و پسورد خودت
ADMIN_INFO = {
    'username': 'mostafazarei',
    'password': 'sn162292856',
    'email': 'mostafazareii@gmail.com',
    'first_name': 'مصطفی',
    'last_name': 'زارعی',
    'phone': '09123456789',  # این رو بعداً به شماره خودت تغییر بده
    'role': 'admin',
}

def create_superuser():
    if not User.objects.filter(username=ADMIN_INFO['username']).exists():
        user = User.objects.create_superuser(
            username=ADMIN_INFO['username'],
            email=ADMIN_INFO['email'],
            password=ADMIN_INFO['password'],
            first_name=ADMIN_INFO['first_name'],
            last_name=ADMIN_INFO['last_name'],
            phone=ADMIN_INFO['phone'],
            role=ADMIN_INFO['role'],
        )
        print(f"✅ ادمین {user.username} ساخته شد!")
        print(f"   رمز عبور: {ADMIN_INFO['password']}")
    else:
        print(f"⚠️ ادمین {ADMIN_INFO['username']} قبلاً ساخته شده")

def create_demo_organizations():
    orgs = [
        {'name': 'آموزشگاه الف', 'slug': 'alef'},
        {'name': 'آموزشگاه ب', 'slug': 'be'},
        {'name': 'آموزشگاه پ', 'slug': 'pe'},
        {'name': 'آموزشگاه ت', 'slug': 'te'},
        {'name': 'آموزشگاه ث', 'slug': 'se'},
    ]
    
    for org in orgs:
        obj, created = Organization.objects.get_or_create(
            slug=org['slug'],
            defaults={'name': org['name'], 'is_active': True}
        )
        if created:
            print(f"✅ سازمان {org['name']} ساخته شد")

if __name__ == '__main__':
    print("🔄 راه‌اندازی سیستم تایتان...")
    create_superuser()
    create_demo_organizations()
    print("✨ کار انجام شد!")
