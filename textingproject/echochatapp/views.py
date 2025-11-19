from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from .models import ChatMessage
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import *

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

@login_required
def create_group(request):
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.owner = request.user     # auto-assign logged-in user
            group.save()
            return redirect("group_created_success")
    else:
        form = CreateGroupForm()

    return render(request, "create_group.html", {"form": form})

def test_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'test.html')
