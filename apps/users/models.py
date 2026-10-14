from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    avatar = models.ImageField(upload_to='users/avatars', default='users/avatars/default.webp')

    enrollment = models.OneToOneField("enrollments.Enrollment", on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return self.username