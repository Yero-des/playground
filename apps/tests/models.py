from django.db import models

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=200)
    url = models.FileField(upload_to="videos", blank=True, null=True)
    description = models.TextField()