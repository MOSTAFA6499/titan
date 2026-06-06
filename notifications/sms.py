import requests
from django.conf import settings
from django.contrib import messages

class SMSService:
    """سرویس ارسال پیامک با کاوه‌نگار"""
    
    @staticmethod
    def send_sms(phone, message):
        """ارسال پیامک به یک شماره"""
        if not settings.KAVENEGAR_API_KEY:
            print("API Key کاوه‌نگار تنظیم نشده است")
            return False
        
        url = f"https://api.kavenegar.com/v1/{settings.KAVENEGAR_API_KEY}/sms/send.json"
        
        data = {
            'receptor': phone,
            'message': message,
        }
        
        try:
            response = requests.post(url, data=data)
            result = response.json()
            
            if response.status_code == 200:
                print(f"پیامک با موفقیت به {phone} ارسال شد")
                return True
            else:
                print(f"خطا در ارسال پیامک: {result}")
                return False
                
        except Exception as e:
            print(f"خطا در ارتباط با سامانه پیامک: {e}")
            return False
    
    @staticmethod
    def send_attendance_alert(student, guardian_phone, status, course_name=None):
        """ارسال پیامک به حامی در صورت غیبت یا تاخیر"""
        
        if status == 'absent':
            message = f"سلام، {student.get_full_name()} امروز در کلاس {course_name if course_name else 'آموزشگاه'} غیبت داشت. لطفاً پیگیری فرمایید."
        elif status == 'late':
            message = f"سلام، {student.get_full_name()} امروز در کلاس {course_name if course_name else 'آموزشگاه'} تأخیر داشت."
        else:
            return False
        
        return SMSService.send_sms(guardian_phone, message)
    
    @staticmethod
    def send_welcome_sms(user):
        """ارسال پیام خوش‌آمدگویی به کاربر جدید"""
        message = f"""سلام {user.get_full_name()}
به سیستم هوشمند تایتان خوش آمدید.
نام کاربری: {user.username}
برای ورود به سایت مراجعه فرمایید."""
        
        return SMSService.send_sms(user.phone, message)
