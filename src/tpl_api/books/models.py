from django.db import models

# Create your models here.
class Book(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=300, blank=True, default='')
    contributors = models.CharField(max_length=200, blank=True, default='')
    branches = models.TextField()

    class Meta:
        ordering = ['created']
