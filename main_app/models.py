from django.db import models

# Create your models here.


class Bird(models.Model):
    name = models.CharField(max_length=250)
    breed = models.CharField(max_length=250)
    description = models.TextField(max_length=250)
    age = models.IntegerField()

    def __str__(self):
        return self.name
