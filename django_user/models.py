from django.db import models

# Create your models here.

class BlackList(models.Model):
    token = models.TextField()