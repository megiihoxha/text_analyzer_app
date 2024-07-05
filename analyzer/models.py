from django.db import models
from django.contrib.auth.models import User


class AnalysisLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    input_text = models.TextField()
    result = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
