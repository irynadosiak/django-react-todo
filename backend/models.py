from django.db import models
from accounts.models import User


class Todo(models.Model):
    text = models.CharField(max_length=256)
    completed = models.BooleanField(default=False)
    owner = models.ForeignKey(User, related_name="todos", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.text
