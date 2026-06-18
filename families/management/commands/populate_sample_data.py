"""
Management command to populate sample Gujarati Samaj data.
Run: python manage.py populate_sample_data
"""
from django.core.management.base import BaseCommand
from families.models import Family, Member, ContactInfo
from events.models import Event
from announcements.models import Announcement
from django.utils import timezone
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Populate database with sample Gujarati Samaj data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')

        # Contact Info
        ContactInfo.objects.get_or_create(
            defaults={
                'samaj_name': 'ગુજરાતી સમાજ',
                'samaj_name_en': 'Gujarati Samaj Community Portal',
                'address': 'સમાજ ભવન, ગુજરાત - 380001\nSamaj Bhavan, Gujarat - 380001',
                'phone': '+91 98765 43210',
                'email': 'info@gujaratisamaj.org',
                'about': 'ગુજરાતી સમાજ - એકતા, સેવા, સંસ્કાર અને સમર્પણ.',
                'founded_year': 1950,
            }
        )

        # Sample Families
        families_data = [
            {
                'family_name': 'કનુભાઈ મગનભાઈ ચૌહાણ',
                'village': 'મોહનપુર',
                'gotra': 'kashyap',
                'address': 'At. Mohanpur, Ta. Wankaner, Dist. Morbi, Gujarat - 363621',
                'mobile': '9876543210',
                'business': 'agriculture',
            },
            {
                'family_name': 'દિલીપભાઈ રમેશભાઈ ચૌહાણ',
                'village': 'ધ્રાંગધ્રા',
                'gotra': 'bharadwaj',
                'address': 'At. Dhrangadhra, Surendranagar, Gujarat',
                'mobile': '9876567890',
                'business': 'business',
            },
            {
                'family_name': 'ભાવેશભાઈ જવેરભાઈ ચૌહાણ',
                'village': 'રાણાસણ',
                'gotra': 'kashyap',
                'address': 'At. Ranashan, Surendranagar, Gujarat',
                'mobile': '9876511223',
                'business': 'service',
            },
            {
                'family_name': 'પ્રવીણભાઈ ભીખાભાઈ પટેલ',
                'village': 'સુરેન્દ્રનગર',
                'gotra': 'atri',
                'address': 'Surendranagar, Gujarat',
                'mobile': '9876598765',
                'business': 'professional',
            },
            {
                'family_name': 'રમેશભાઈ મનસુખભાઈ દેસાઈ',
                'village': 'હળવદ',
                'gotra': 'vasishtha',
                'address': 'At. Halvad, Morbi, Gujarat',
                'mobile': '9876512345',
                'business': 'agriculture',
            },
        ]

        for fdata in families_data:
            family, created = Family.objects.get_or_create(
                family_name=fdata['family_name'],
                defaults=fdata
            )
            if created:
                self.stdout.write(f'  ✓ Created family: {family.family_name}')

                # Add members for each family
                members = [
                    {'name': fdata['family_name'].split()[0], 'relation': 'head', 'gender': 'male', 'education': '10th', 'occupation': fdata['business'].capitalize()},
                    {'name': 'પત્ની ' + fdata['family_name'].split()[0], 'relation': 'wife', 'gender': 'female', 'education': '8th', 'occupation': 'Housewife'},
                    {'name': 'પુત્ર ' + fdata['family_name'].split()[0], 'relation': 'son', 'gender': 'male', 'education': 'B.Com', 'occupation': 'Student'},
                ]
                for mdata in members:
                    Member.objects.create(family=family, **mdata)

        # Sample Events
        today = date.today()
        events_data = [
            {
                'title': 'સમૂહ લગ્નોત્સવ 2025',
                'description': 'ગુજરાતી સમાજ દ્વારા આયોજિત વાર્ષિક સમૂહ લગ્ન સમારોહ. Annual community wedding ceremony organized by Gujarati Samaj.',
                'event_date': today + timedelta(days=15),
                'event_time': '09:00:00',
                'location': 'સમાજ ભવન, ગુજરાત / Samaj Bhavan, Gujarat',
            },
            {
                'title': 'સ્નેહ મિલન - 2025',
                'description': 'સ્નેહ મિલન - સૌ સભ્યો સાથે મળીએ. Community get-together event for all members and families.',
                'event_date': today + timedelta(days=30),
                'event_time': '17:00:00',
                'location': 'સમાજ ભવન, ગુજરાત / Samaj Bhavan',
            },
            {
                'title': 'યુવા સંમેલન 2025',
                'description': 'યુવા પ્રતિભાઓ માટે વિશેષ સંમેલન. Special youth convention for young talents of our community.',
                'event_date': today + timedelta(days=45),
                'event_time': '10:00:00',
                'location': 'ટાઉન હૉલ, ગુજરાત / Town Hall, Gujarat',
            },
            {
                'title': 'દીપોત્સવ ઉત્સવ 2024',
                'description': 'સમાજ દ્વારા ઉજવાયો દિવાળી ઉત્સવ. Diwali celebration organized by the samaj.',
                'event_date': today - timedelta(days=60),
                'location': 'સમાજ ભવન, ગુજરાત',
            },
        ]

        for edata in events_data:
            event, created = Event.objects.get_or_create(
                title=edata['title'],
                defaults=edata
            )
            if created:
                self.stdout.write(f'  ✓ Created event: {event.title}')

        # Sample Announcements
        announcements_data = [
            {
                'title': 'સભ્ય નોંધણી ખુલ્લી / Member Registration Open',
                'description': 'નવા સભ્યોની નોંધણી ૩૧ ડિસેમ્બર ૨૦૨૫ સુધી ખુલ્લી છે. New member registration is open until December 31, 2025. Please contact the office for details.',
                'publish_date': today,
            },
            {
                'title': 'સમૂહ લગ્ન - ફોર્મ ભરો / Fill Samuh Lagna Form',
                'description': 'સમૂહ લગ્ન ૨૦૨૫ માટે ફોર્મ ભરવાની છેલ્લી તારીખ ૩૧ જાન્યુઆરી ૨૦૨૫ છે. Forms for Samuh Lagna 2025 must be submitted by January 31, 2025.',
                'publish_date': today - timedelta(days=5),
            },
            {
                'title': 'વાર્ષિક સભા / Annual Meeting Notice',
                'description': 'વાર્ષિક સભા ૧૫ ફેબ્રુઆરી ૨૦૨૫ ના રોજ સવારે ૧૦:૦૦ વાગ્યે. Annual meeting on February 15, 2025 at 10:00 AM at Samaj Bhavan.',
                'publish_date': today - timedelta(days=10),
            },
        ]

        for adata in announcements_data:
            ann, created = Announcement.objects.get_or_create(
                title=adata['title'],
                defaults=adata
            )
            if created:
                self.stdout.write(f'  ✓ Created announcement: {ann.title}')

        self.stdout.write(self.style.SUCCESS('\n✅ Sample data created successfully!'))
        self.stdout.write('  Run: python manage.py createsuperuser  (to create admin user)')
        self.stdout.write('  Then visit: http://127.0.0.1:8000/dashboard/ (after login)')
