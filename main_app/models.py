from django.db import models

# Create your models here.

MEALS = (("B", "Breakfast"), ("L", "Lunch"), ("D", "Dinner"))


class Bird(models.Model):
    name = models.CharField(max_length=250)
    breed = models.CharField(max_length=250)
    description = models.TextField(max_length=250)
    age = models.IntegerField()

    def __str__(self):
        return self.name


class Feeding(models.Model):
    date = models.DateField("feeding date")
    meal = models.CharField(max_length=1, choices=MEALS, default=MEALS[0][0])
    bird = models.ForeignKey(Bird, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_meal_display()} on {self.date}"
