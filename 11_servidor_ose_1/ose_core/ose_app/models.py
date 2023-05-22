from django.db import models

# Create your models here.

class Meassure(models.Model):
    name = models.CharField(max_length=100)
    flow = models.FloatField()
    location = models.TextField()

    def __str__(self):
        return self.name
