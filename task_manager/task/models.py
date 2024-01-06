from django.db import models
from django.contrib.auth import get_user_model
import os 
userModel = get_user_model()
from datetime import date

priorities = (
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
)


class Task(models.Model):
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=priorities)
    due_date = models.DateField(default=date.today(), null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(userModel, on_delete=models.CASCADE, related_name='task')
    image = models.ImageField(upload_to='Api/task_images', null=True, blank=True)
    def delete(self, *args, **kwargs):
        if self.image:
            storage, path = self.image.storage, self.image.path
            if storage.exists(path):
                storage.delete(path)

        super(Task, self).delete(*args, **kwargs)
