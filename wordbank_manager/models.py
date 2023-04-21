from django.db import models
from django.contrib.auth.models import User


class Prompt(models.Model):
    CATEGORY_CHOICES = [
        ('small_talk', 'Small Talk'),
        ('technical', 'Technical'),
        ('behavioral', 'Behavioral')
    ]
    text = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    hashtags = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.text
