from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseUser(AbstractUser):
    profile = models.ImageField(upload_to='users', default='users/default.jfif')

    # RS
    # contacts


class ContactType(models.Model):
    name = models.CharField(max_length=50)

    # RS
    # contacts

    def __str__(self) -> str:
        return self.name


class Contact(models.Model):
    value = models.CharField(max_length=100)

    type = models.ForeignKey(ContactType, on_delete=models.CASCADE, related_name='contacts')
    owner = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='contacts')

    def __str__(self) -> str:
        return f"{self.owner} - {self.type}: {self.value}"
