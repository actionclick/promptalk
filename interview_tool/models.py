from django.db import models
from django.contrib.auth.models import User
from wordbank_manager.models import Prompt

class Interview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Interview {self.id} ({self.user.username})"

class Response(models.Model):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE)
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response {self.id} ({self.interview}, {self.prompt})"



