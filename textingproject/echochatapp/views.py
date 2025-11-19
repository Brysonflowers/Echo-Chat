from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from .models import ChatMessage
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/sign_up.html"

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        for field in form.fields.values():
            field.help_text = None
        return form

def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")

def thecurrentchatviewer(request: HttpRequest) -> HttpResponse:
    messages = ChatMessage.objects.order_by('timestamp').all()[:10]
    return render(request, "chattextpage.html", {'messages': messages})