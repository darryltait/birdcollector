from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Bird

# from django.http import HttpResponse

# Create your views here.


def home(request):
    return render(request, "home.html")
    # return HttpResponse("<h1>Hello World</h1>")


def about(request):
    # return HttpResponse("<h1>About the Bird Collector</h1>")
    return render(request, "about.html")


def birds_index(request):
    birds = Bird.objects.all()
    return render(request, "birds/index.html", {"birds": birds})


def birds_detail(request, bird_id):
    bird = Bird.objects.get(id=bird_id)
    return render(request, "birds/detail.html", {"bird": bird})


class BirdCreate(CreateView):
    model = Bird
    fields = "__all__"
    #  can redirect like below, but it's better to add a return in Model
    # success_url = "/birds/"


class BirdUpdate(UpdateView):
    model = Bird
    fields = ["breed", "description", "age"]


class BirdDelete(DeleteView):
    model = Bird
    success_url = "/birds/"
