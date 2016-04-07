import uuid
from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    email = models.EmailField(max_length=255)
    name = models.CharField (max_length=255)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    access_token = models.UUIDField(default=uuid.uuid4)

    # def save(self, *args, **kwargs):
    #     self.updated_at = timezone.now()
    #     return super().save(*args, **kwargs)