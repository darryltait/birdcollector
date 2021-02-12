from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.


class Bird:
    def __init__(self, name, breed, description, age):
        self.name = name
        self.breed = breed
        self.description = description
        self.age = age


birds = [
    Bird("Nimbus", "gray", "sweet", 5),
    Bird("Ghost", "orange", "fat", 12),
    Bird("Bon Bon", "maine coon", "the boss", 0),
    Bird("Pancho", "yellow-nape", "a talker!", 7),
]


def home(request):
    return render(request, "home.html")
    # return HttpResponse("<h1>Hello World</h1>")


def about(request):
    # return HttpResponse("<h1>About the Bird Collector</h1>")
    return render(request, "about.html")


def index(request):
    return render(request, "birds/index.html", {"birds": birds})
