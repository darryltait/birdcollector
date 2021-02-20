from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Bird
from .models import Toy
from .forms import FeedingForm

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
    toys_bird_doesnt_have = Toy.objects.exclude(
        id__in=bird.toys.all().values_list("id")
    )
    feeding_form = FeedingForm()
    return render(
        request,
        "birds/detail.html",
        {"bird": bird, "feeding_form": feeding_form, "toys": toys_bird_doesnt_have},
    )


class BirdCreate(CreateView):
    model = Bird
    # fields = "__all__"
    fields = ["name", "breed", "description", "age"]
    #  can redirect like below, but it's better to add a return in Model
    # success_url = "/birds/"


class BirdUpdate(UpdateView):
    model = Bird
    fields = ["breed", "description", "age"]


class BirdDelete(DeleteView):
    model = Bird
    success_url = "/birds/"


def add_feeding(request, bird_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.bird_id = bird_id
        new_feeding.save()
    return redirect("detail", bird_id=bird_id)


def toys_index(request):
    toys = Toy.objects.all()
    return render(request, "toys/index.html", {"toys": toys})


def toys_detail(request, toy_id):
    toy = Toy.objects.get(id=toy_id)
    return render(request, "toys/detail.html", {"toy": toy})


class ToyCreate(CreateView):
    model = Toy
    fields = "__all__"


class ToyUpdate(UpdateView):
    model = Toy
    fields = "__all__"


class ToyDelete(DeleteView):
    model = Toy
    success_url = "/toys/"


def assoc_toy(request, bird_id, toy_id):
    Bird.objects.get(id=bird_id).toys.add(toy_id)
    return redirect("detail", bird_id=bird_id)
