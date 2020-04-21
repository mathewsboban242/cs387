from django.db import models

class Idea(models.Model):
    content = models.CharField(max_length=1000)
