from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse

# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")