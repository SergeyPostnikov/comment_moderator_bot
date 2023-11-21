from django.db import models
from django.utils import timezone as tz


class Comment(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создан'),
        ('published', 'Опубликован'),
    ]

    created_at = models.DateTimeField(default=tz.now)

    text = models.TextField()
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='created'
    )

    def __str__(self):
        return f"{self.text[:50]}..."
