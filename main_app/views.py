# package for generating unique keys for the photos
import uuid

# AWS SDK package
import boto3


from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# use sessions to log the user in
from django.contrib.auth import login

# display user inputs in a form
from django.contrib.auth.forms import UserCreationForm

# login required decorator
from django.contrib.auth.decorators import login_required

# login required mixin for class based view
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Bird, Toy, Photo
from .forms import FeedingForm

# format should be 'protocol://service-code.region-code.amazonaws.com'
S3_BASE_URL = "https://s3.us-east-2.amazonaws.com/"
BUCKET = "dareal-birdcollector"


def signup(request):
    error_message = ""

    if request.method == "POST":
        # Create the user using UserCreateForm
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # actually save the user if form data is valid
            user = form.save()
            # actually log the user in (session-based)
            login(request, user)
            return redirect("index")
        else:
            error_message = "Invalid data for sign up"

    # if a bad POST request, or a normal GET request, send errors to sign up template
    form = UserCreationForm()
    context = {"form": form, "error_message": error_message}
    return render(request, "registration/signup.html", context)


# from django.http import HttpResponse

# Create your views here.


def home(request):
    return render(request, "home.html")
    # return HttpResponse("<h1>Hello World</h1>")


def about(request):
    # return HttpResponse("<h1>About the Bird Collector</h1>")
    return render(request, "about.html")


@login_required
def birds_index(request):
    # Finds all the birds, regardless of user
    # birds = Bird.objects.all()

    # this filters to find only the birds owned by the logged in user
    birds = Bird.objects.filter(user=request.user)
    return render(request, "birds/index.html", {"birds": birds})


@login_required
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


class BirdCreate(LoginRequiredMixin, CreateView):
    model = Bird
    # fields = "__all__"
    fields = ["name", "breed", "description", "age"]
    #  can redirect like below, but it's better to add a return in Model
    # success_url = "/birds/"
    # override form_valid to attach the user to the cat before form data is saved
    def form_valid(self, form):
        # the bird data will be stored in 'form.instance'
        # self.request.user will be the currently logged in user
        form.instance.user = self.request.user
        # allowing CreateView parent class to handle the rest
        return super().form_valid(form)


class BirdUpdate(LoginRequiredMixin, UpdateView):
    model = Bird
    fields = ["breed", "description", "age"]


class BirdDelete(LoginRequiredMixin, DeleteView):
    model = Bird
    success_url = "/birds/"


@login_required
def add_feeding(request, bird_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.bird_id = bird_id
        new_feeding.save()
    return redirect("detail", bird_id=bird_id)


@login_required
def toys_index(request):
    toys = Toy.objects.all()
    return render(request, "toys/index.html", {"toys": toys})


@login_required
def toys_detail(request, toy_id):
    toy = Toy.objects.get(id=toy_id)
    return render(request, "toys/detail.html", {"toy": toy})


class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = "__all__"


class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = "__all__"


class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = "/toys/"


@login_required
def assoc_toy(request, bird_id, toy_id):
    Bird.objects.get(id=bird_id).toys.add(toy_id)
    return redirect("detail", bird_id=bird_id)


# add @login_required when unassoc_toy is added
@login_required
def unassoc_toy(request, bird_id, toy_id):
    Bird.objects.get(id=bird_id).toys.remove(toy_id)
    return redirect("detail", bird_id=bird_id)


@login_required
def add_photo(request, bird_id):
    # the <input> will have 'name' attribute- that's the key our file will be on the incoming data
    photo_file = request.FILES.get("photo_file", None)

    if photo_file:
        # create an s3 instance
        s3 = boto3.client("s3")
        # generate a unique key for the image
        # variable to store index of the dot before the file extension
        # rfind will find the last instance of the '.' character
        index_of_last_period = photo_file.name.rfind(".")
        # generate a unique key and grab the first 6 characters of it
        # GEffed.png
        key = uuid.uuid4().hex[:6] + photo_file.name[index_of_last_period:]

        try:
            # s3 client - attempt to perform a file upload
            s3.upload_fileobj(photo_file, BUCKET, key)

            # generate the url based on the key name, our base url and bucket
            url = f"{S3_BASE_URL}{BUCKET}/{key}"

            photo = Photo(url=url, bird_id=bird_id)
            photo.save()
        except:
            print("An error occurred uploading files to AWS")

    # return redirect("bird", bird_id=bird_id)
    # return redirect("birds_detail", bird_id=bird_id)
    # return redirect("birds/detail.html", bird_id=bird_id)
    return redirect("detail", bird_id=bird_id)
