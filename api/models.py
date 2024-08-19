from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    # the task model, link to the default django user model,
    # the will only be able to update the title, descriṕtion and completed fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.description
    
