from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from .models import ChatMessage

# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")

def thecurrentchatviewer(request: HttpRequest) -> HttpResponse:
    messages = ChatMessage.objects.order_by('timestamp').all()[:10]
    return render(request, "chattextpage.html", {'messages': messages})
