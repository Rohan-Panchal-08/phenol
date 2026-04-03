from django.db import models

SERVICE_CHOICES = [
    ('swedish_massage', 'Swedish Massage'),
    ('deep_tissue', 'Deep Tissue Massage'),
    ('hot_stone', 'Hot Stone Therapy'),
    ('aromatherapy', 'Aromatherapy Massage'),
    ('facial', 'Luxury Facial'),
    ('body_wrap', 'Body Wrap Treatment'),
    ('foot_reflexology', 'Foot Reflexology'),
    ('couples_massage', 'Couples Massage'),
    ('prenatal_massage', 'Prenatal Massage'),
    ('sports_massage', 'Sports Massage'),
]

DURATION_CHOICES = [
    ('30', '30 Minutes'),
    ('60', '60 Minutes'),
    ('90', '90 Minutes'),
    ('120', '120 Minutes'),
]

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('prefer_not', 'Prefer Not to Say'),
]

THERAPIST_CHOICES = [
    ('any', 'No Preference'),
    ('female', 'Female Therapist'),
    ('male', 'Male Therapist'),
]

class Booking(models.Model):
    # Personal Info
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='prefer_not')

    # Booking Details
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    therapist_preference = models.CharField(max_length=20, choices=THERAPIST_CHOICES, default='any')

    # Health & Preferences
    health_conditions = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    pressure_preference = models.CharField(max_length=20, choices=[
        ('light', 'Light'),
        ('medium', 'Medium'),
        ('firm', 'Firm'),
        ('deep', 'Deep'),
    ], default='medium')
    special_requests = models.TextField(blank=True, null=True)

    # Consent
    consent_given = models.BooleanField(default=False)

    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    exported = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.service} on {self.preferred_date}"

    def get_service_display_name(self):
        return dict(SERVICE_CHOICES).get(self.service, self.service)

    def get_duration_display_name(self):
        return dict(DURATION_CHOICES).get(self.duration, self.duration)
