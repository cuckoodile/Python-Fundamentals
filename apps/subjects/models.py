from django.db import models

# Create your models here.

class Section(models.Model):
    name = models.CharField(max_length=50)   # Optional
    thumbnail = models.ImageField(upload_to='sections', default='sections/default.webp')

    # Relationships
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name="sections")

    # Reverse Calls or RC
    # students

class Subjects(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='subjects/', default='subjects/default.webp')
    is_core = models.BooleanField(default=False, blank=True)

    course = models.ManyToManyField('Course', related_name='subjects')

class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, null=True, blank=True)    # Optional
    thumbnail = models.ImageField(upload_to='courses', default='courses/default.webp')

    # Reverse Calls
    # sections
    # subjects