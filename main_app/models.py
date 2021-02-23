from django.db import models
from django.urls import reverse
from datetime import date

# import the built-in User model from django library

# Create your models here.

MEALS = (("B", "Breakfast"), ("L", "Lunch"), ("D", "Dinner"))


class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("toys_detail", kwargs={"toy_id": self.id})
        # return reverse("toys_detail", kwargs={"pk": self.id})

    class Meta:
        ordering = ["name"]


class Bird(models.Model):
    name = models.CharField(max_length=250)
    breed = models.CharField(max_length=250)
    description = models.TextField(max_length=250)
    age = models.IntegerField()

    toys = models.ManyToManyField(Toy)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("detail", kwargs={"bird_id": self.id})

    def fed_for_today(self):
        return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)


class Feeding(models.Model):
    date = models.DateField("feeding date")
    meal = models.CharField(max_length=1, choices=MEALS, default=MEALS[0][0])
    bird = models.ForeignKey(Bird, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_meal_display()} on {self.date}"

    class Meta:
        ordering = ["-date"]


class Photo(models.Model):
    # store the url of image on aws
    url = models.CharField(max_length=200)
    # relationship to the cat
    bird = models.ForeignKey(Bird, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for cat id # {self.cat_id} @ {self.url}"