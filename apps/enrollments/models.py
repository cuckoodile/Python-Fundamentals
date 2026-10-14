from django.db import models

from apps.subjects.models import Section

# Create your models here.

class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('e', 'Enrolled'),
        ('p', 'Pending'),
        ('d', 'Dropped'),
        ('c', 'Completed'),
    ]

    # 2027-2028
    school_year = models.CharField(max_length=9)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)