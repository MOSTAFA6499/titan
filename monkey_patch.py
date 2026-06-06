# monkey_patch.py
from django.db.models import ForeignKey, CASCADE
from django.conf import settings

def patch_organizations():
    """رفع خطای تداخل فیلدها در django-organizations"""
    try:
        from organizations.models import Team
        
        # چک کردن اینکه آیا related_name قبلاً تنظیم شده یا نه
        field = Team._meta.get_field('leader')
        if not hasattr(field, 'remote_field') or field.remote_field.related_name is None:
            # پچ کردن فیلد leader
            leader_field = ForeignKey(
                settings.AUTH_USER_MODEL,
                on_delete=CASCADE,
                related_name='leading_teams',  # related_name دلخواه
                null=True,
                blank=True
            )
            Team._meta.fields = [f for f in Team._meta.fields if f.name != 'leader']
            Team._meta.local_fields = [f for f in Team._meta.local_fields if f.name != 'leader']
            Team.add_to_class('leader', leader_field)
            print("✅ organizations.Team.leader patched successfully")
    except ImportError:
        print("⚠️ organizations app not found, skipping patch")
    except Exception as e:
        print(f"❌ Patch failed: {e}")
