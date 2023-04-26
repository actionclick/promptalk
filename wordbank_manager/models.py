from django.db import models
from django.contrib.auth.models import User


class StandardPrompt(models.Model):
    CATEGORY_CHOICES = [
        ('small_talk', 'Small Talk'),
        ('technical', 'Technical'),
        ('behavioral', 'Behavioral')
    ]
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    hashtags = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.text

class PromptCategory(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prompt_categories')

    def __str__(self):
        return self.name
class UserPrompt(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    category = models.ManyToManyField(PromptCategory, blank=True)
    hashtags = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.text