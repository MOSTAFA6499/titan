from django.db.models.signals import post_save
from django.dispatch import receiver
from attendance.models import Attendance
from .sms import SMSService

@receiver(post_save, sender=Attendance)
def send_sms_on_absence(sender, instance, created, **kwargs):
    """
    وقتی حضور و غیاب جدید ثبت شد،
    اگر وضعیت غایب یا تأخیر بود، به حامی پیامک بفرست
    """
    if created and instance.status in ['absent', 'late']:
        student = instance.user
        guardian_phone = student.guardian_phone
        
        if guardian_phone:
            course_name = instance.course.title if instance.course else None
            SMSService.send_attendance_alert(
                student=student,
                guardian_phone=guardian_phone,
                status=instance.status,
                course_name=course_name
            )
