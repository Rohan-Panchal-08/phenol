from django.db import models



CLIENT_TYPE_CHOICES = [
    ('female', 'Female'),
    ('couple', 'Couple'),
]

SERVICE_CHOICES = [
    ('foot_massage',     'Foot Massage'),
    ('head_massage',     'Head Massage'),
    ('thigh_massage',    'Thigh Massage'),
    ('shoulder_massage', 'Shoulder Massage'),
    ('back_massage',     'Back Massage'),
]
DURATION_CHOICES = [
    ('30','30 Minutes'),('60','60 Minutes'),('90','90 Minutes'),('120','120 Minutes'),
]
# GENDER_CHOICES   = [('male','Male'),('female','Female'),('prefer_not','Prefer Not to Say')]
# THERAPIST_CHOICES= [('any','No Preference'),('female','Female Therapist'),('male','Male Therapist')]
PRESSURE_CHOICES = [('light','Light'),('medium','Medium'),('firm','Firm'),('deep','Deep')]
RATING_CHOICES   = [(i,str(i)) for i in range(1,6)]



STATUS_CHOICES = [
    ('confirmed', 'Confirmed'),
    ('cancelled', 'Cancelled'),
    ('postponed', 'Postponed'),
]

status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')

class Booking(models.Model):
    full_name            = models.CharField(max_length=200)
    email                = models.EmailField()
    phone                = models.CharField(max_length=20)
    date_of_birth        = models.DateField(null=True, blank=True)
    partner_name = models.CharField(max_length=200, null=True, blank=True)
    partner_age = models.IntegerField(null=True, blank=True)
    partner_gender = models.CharField(max_length=10, null=True, blank=True)

    client_type          = models.CharField(max_length=20, choices=CLIENT_TYPE_CHOICES)

    service              = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    duration             = models.CharField(max_length=10, choices=DURATION_CHOICES, default='60')

    preferred_date       = models.DateField()
    preferred_time       = models.TimeField()

    health_conditions    = models.TextField(blank=True, null=True)
    allergies            = models.TextField(blank=True, null=True)

    pressure_preference  = models.CharField(max_length=20, choices=PRESSURE_CHOICES, default='medium')
    special_requests     = models.TextField(blank=True, null=True)

    consent_given        = models.BooleanField(default=False)

    # ✅ NEW FIELD (correct placement)
    status               = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')

    created_at           = models.DateTimeField(auto_now_add=True)

    partner_name = models.CharField(max_length=200, null=True, blank=True)
    partner_age = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['preferred_date', 'preferred_time'],
                name='unique_booking_slot'
            )
        ]

    def __str__(self):
        return f"{self.full_name} — {self.service} on {self.preferred_date}"


class Review(models.Model):
    name       = models.CharField(max_length=100)
    service    = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    rating     = models.IntegerField(choices=RATING_CHOICES, default=5)
    comment    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved   = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.rating}★"


class SiteVisit(models.Model):
    """One row per page visit — used for daily/monthly/yearly analytics."""
    visited_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ['-visited_at']

    def __str__(self):
        return str(self.visited_at)
