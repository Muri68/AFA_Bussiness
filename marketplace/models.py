from django.db import models
from django.utils import timezone

# Create your models here.
class NewsLetterUsers(models.Model):
    email = models.CharField(unique=True, max_length=100)
    created_date = models.DateTimeField('Date created', default=timezone.now)
    
    def __str__(self):
        return self.email