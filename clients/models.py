from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

# Create your models here.
class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to="avatars/", default='avatars/default.jpg')

    @property
    def age(self):
        if not self.birth_date:
            return None

        today = date.today()

        year = today.year - self.birth_date.year
        had_birth_day = (today.month, today.day) < (self.birth_date.month, self.birth_date.day)

        return year - 1 if had_birth_day else year