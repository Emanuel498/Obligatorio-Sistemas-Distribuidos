from django.db import models

class Data(models.Model):
    name = models.CharField(max_length=100)
    flow = models.FloatField()
    location = models.TextField()

    def __str__(self):
        return self.name
