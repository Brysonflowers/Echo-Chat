from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from .models import ChatMessage
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")

@login_required
def thecurrentchatviewer(request: HttpRequest) -> HttpResponse:
    messages = ChatMessage.objects.order_by('timestamp').all()[:25]
    friends = [] # an empty list for now
    return render(request, "chats.html", {'messages': messages, 'friends': friends})