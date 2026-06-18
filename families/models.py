from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


GOTRA_CHOICES = [
    ('kashyap', 'કાશ્યપ / Kashyap'),
    ('bharadwaj', 'ભારદ્વાજ / Bharadwaj'),
    ('atri', 'અત્રિ / Atri'),
    ('vasishtha', 'વસિષ્ઠ / Vasishtha'),
    ('vishwamitra', 'વિશ્વામિત્ર / Vishwamitra'),
    ('other', 'અન્ય / Other'),
]

BUSINESS_CHOICES = [
    ('agriculture', 'કૃષિ / Agriculture'),
    ('business', 'વ્યવસાય / Business'),
    ('service', 'નોકરી / Service'),
    ('professional', 'વ્યવસાયિક / Professional'),
    ('other', 'અન્ય / Other'),
]

RELATION_CHOICES = [
    ('head', 'મુખ્ય / Head'),
    ('wife', 'પત્ની / Wife'),
    ('son', 'પુત્ર / Son'),
    ('daughter', 'પુત્રી / Daughter'),
    ('daughter_in_law', 'પુત્રવધૂ / Daughter-in-law'),
    ('son_in_law', 'જમાઈ / Son-in-law'),
    ('father', 'પિતા / Father'),
    ('mother', 'માતા / Mother'),
    ('brother', 'ભાઈ / Brother'),
    ('sister', 'બહેન / Sister'),
    ('grandfather', 'દાદા / Grandfather'),
    ('grandmother', 'દાદી / Grandmother'),
    ('grandson', 'પૌત્ર / Grandson'),
    ('granddaughter', 'પૌત્રી / Granddaughter'),
    ('uncle', 'કાકા / Uncle'),
    ('aunt', 'કાકી / Aunt'),
    ('other', 'અન્ય / Other'),
]

GENDER_CHOICES = [
    ('male', 'પુરુષ / Male'),
    ('female', 'સ્ત્રી / Female'),
    ('other', 'અન્ય / Other'),
]

MARITAL_STATUS_CHOICES = [
    ('unmarried', 'અવિવાહિત / Unmarried'),
    ('married', 'વિવાહિત / Married'),
    ('widowed', 'વિધવા/વિધુર / Widowed'),
    ('divorced', 'છૂટાછેડા / Divorced'),
]

BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
    ('O+', 'O+'), ('O-', 'O-'),
    ('unknown', 'Unknown'),
]

EDUCATION_CHOICES = [
    ('below_5th', 'Below 5th'),
    ('5th', '5th Pass'),
    ('8th', '8th Pass'),
    ('10th', '10th Pass (SSC)'),
    ('12th', '12th Pass (HSC)'),
    ('diploma', 'Diploma'),
    ('graduate', 'Graduate (B.A/B.Com/B.Sc)'),
    ('engineering', 'B.E / B.Tech'),
    ('medical', 'MBBS / Medical'),
    ('postgraduate', 'Post Graduate (M.A/M.Com/M.Sc)'),
    ('mba', 'MBA'),
    ('phd', 'PhD / Doctorate'),
    ('other', 'Other'),
]


class Family(models.Model):
    submitted_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='families', verbose_name='Submitted By'
    )
    family_name = models.CharField(max_length=200, verbose_name='કુટુંબ નામ / Family Name')
    village = models.CharField(max_length=200, verbose_name='ગામ / Village')
    gotra = models.CharField(max_length=100, choices=GOTRA_CHOICES, verbose_name='ગોત્ર / Gotra')
    address = models.TextField(verbose_name='સરનામું / Address')
    mobile = models.CharField(max_length=15, verbose_name='મોબાઈલ / Mobile')
    email = models.EmailField(blank=True, verbose_name='ઈ-મેઈલ / Email')
    business = models.CharField(max_length=100, choices=BUSINESS_CHOICES, verbose_name='વ્યવસાય / Business')
    family_photo = models.ImageField(upload_to='family_photos/', blank=True, null=True, verbose_name='કુટુંબ ફોટો')
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Family / કુટુંબ'
        verbose_name_plural = 'Families / કુટુંબો'
        ordering = ['family_name']

    def __str__(self):
        return f"{self.family_name} - {self.village}"

    def member_count(self):
        return self.members.filter(is_active=True).count()

    @property
    def family_id(self):
        return f"GSM-{self.pk:04d}"


class Member(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='members', verbose_name='કુટુંબ / Family')

    # Basic Info
    name = models.CharField(max_length=200, verbose_name='નામ / Name')
    relation = models.CharField(max_length=50, choices=RELATION_CHOICES, verbose_name='સંબંધ / Relation')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='જાતિ / Gender')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='જન્મ તારીખ / Date of Birth')
    marital_status = models.CharField(
        max_length=20, choices=MARITAL_STATUS_CHOICES,
        default='unmarried', verbose_name='વૈવાહિક સ્થિતિ / Marital Status'
    )

    # Contact
    mobile = models.CharField(max_length=15, blank=True, verbose_name='મોબાઈલ / Mobile')
    whatsapp = models.CharField(max_length=15, blank=True, verbose_name='WhatsApp નં.')
    email = models.EmailField(blank=True, verbose_name='ઈ-મેઈલ / Email')

    # Education & Work
    education = models.CharField(
        max_length=50, choices=EDUCATION_CHOICES, blank=True,
        verbose_name='શિક્ષણ / Education'
    )
    education_detail = models.CharField(
        max_length=200, blank=True,
        verbose_name='શિક્ષણ વિગત / Education Detail',
        help_text='e.g. B.Com from Gujarat University 2020'
    )
    occupation = models.CharField(max_length=200, blank=True, verbose_name='વ્યવસાય / Occupation')
    occupation_detail = models.CharField(
        max_length=200, blank=True,
        verbose_name='કામ વિગત / Work Detail',
        help_text='e.g. Software Engineer at TCS, Ahmedabad'
    )
    annual_income = models.CharField(
        max_length=50, blank=True,
        verbose_name='વાર્ષિક આવક / Annual Income',
        help_text='e.g. 3-5 Lakh, 5-10 Lakh'
    )

    # Health
    blood_group = models.CharField(
        max_length=10, choices=BLOOD_GROUP_CHOICES,
        blank=True, verbose_name='બ્લડ ગ્રૂપ / Blood Group'
    )
    any_disability = models.BooleanField(default=False, verbose_name='અપંગતા / Any Disability')
    disability_detail = models.CharField(max_length=200, blank=True, verbose_name='અપંગતા વિગત')

    # Marriage-specific (for married members)
    spouse_name = models.CharField(max_length=200, blank=True, verbose_name='જીવનસાથી નામ / Spouse Name')
    marriage_date = models.DateField(null=True, blank=True, verbose_name='લગ્ન તારીખ / Marriage Date')

    # Photo
    photo = models.ImageField(upload_to='member_photos/', blank=True, null=True, verbose_name='ફોટો / Photo')

    # Soft delete
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Member / સભ્ય'
        verbose_name_plural = 'Members / સભ્યો'
        ordering = ['relation', 'name']

    def __str__(self):
        return f"{self.name} ({self.family.family_name})"

    @property
    def age(self):
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None

    @property
    def birthday_this_month(self):
        if self.date_of_birth:
            from datetime import date
            return self.date_of_birth.month == date.today().month
        return False


class ContactInfo(models.Model):
    samaj_name = models.CharField(max_length=300, default='ગુજરાતી સમાજ')
    samaj_name_en = models.CharField(max_length=300, default='Gujarati Samaj')
    address = models.TextField(verbose_name='સરનામું / Address')
    phone = models.CharField(max_length=20, verbose_name='ફોન / Phone')
    email = models.EmailField(verbose_name='ઈ-મેઈલ / Email')
    about = models.TextField(blank=True, verbose_name='સમાજ વિશે / About Samaj')
    map_embed_url = models.URLField(blank=True, verbose_name='Google Map URL')
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    founded_year = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Contact Info'
        verbose_name_plural = 'Contact Info'

    def __str__(self):
        return self.samaj_name
