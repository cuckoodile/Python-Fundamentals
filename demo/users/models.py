from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/', default='avatar/default.webp')
    # models.CharField(_(""), max_length=50)
    # avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)
