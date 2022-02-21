from django.db import models

# Create your models here.
class Book(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='books', on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=300, blank=True, default='')
    query = models.CharField(max_length=300, blank=True, default='')
    contributors = models.CharField(max_length=200, blank=True, default='')
    branches = models.TextField()

    class Meta:
        ordering = ['created']