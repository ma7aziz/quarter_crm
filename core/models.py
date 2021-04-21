from django.db import models
from accounts.models import User
# Create your models here.

# MODEL TASK


class TaskManager(models.Manager):
    def open(self):
        return self.filter(status="open")


class Task(models.Model):
    TASK_STATUS = [
        ("open", "open"),
        ("closed", "closed")
    ]
    title = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="task_added_by", null=True)
    employee = models.ForeignKey(
        User, on_delete=models.CASCADE)
    details = models.TextField(max_length=500, blank=True, null=True)
    files = models.FileField(upload_to='tasks/files', blank=True, null=True)
    due_date = models.DateTimeField()
    status = models.CharField(
        max_length=10, choices=TASK_STATUS, default="open")
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = TaskManager()

    def __str__(self):
        return f"{self.title} for {self.employee}"
