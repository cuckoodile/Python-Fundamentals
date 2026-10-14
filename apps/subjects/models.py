from django.db import models

# Create your models here.

class Section(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, null=True, blank=True)    # Optional
    thumbnail = models.ImageField(upload_to='sections', default='sections/default.webp')

    # Relationships
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name="sections")

    # Reverse Calls or RC
    # students

class Subjects(models.Model):
    pass

class Course(models.Model):
    pass

    # Reverse Calls
    # sections