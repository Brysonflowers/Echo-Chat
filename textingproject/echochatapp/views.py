from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/sign_up.html"

# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")