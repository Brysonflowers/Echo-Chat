from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from django.http import HttpResponse
from .models import Message, ChatGroup
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import *

# Source - https://stackoverflow.com/a
# Posted by Brandon Taylor, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-19, License - CC BY-SA 4.0
from django.contrib.auth import get_user_model
User = get_user_model()


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

@login_required
def thecurrentchatviewer(request: HttpRequest, room_name: str) -> HttpResponse:
    chat_group = get_object_or_404(ChatGroup, name=room_name)
    messages = Message.objects.filter(group=chat_group).order_by('timestamp').all()[:10]
    return render(request, "chattextpage.html", {'room_name': room_name, 'messages': messages})

@login_required
def create_group(request: HttpRequest):
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

def private_chats_view(request: HttpRequest) -> HttpResponse:
    users = User.objects.all()
    name_form = SearchUserForm()
    user = 'no name form'
    empty_dict = {}
    if request.POST != empty_dict:
        user = request.POST['name']
        try:
            user = users.get(username = user)
        except:
            user = 'none'

    return render(request, 'private chat.html', {'users': users, 'name_form': name_form, 'user': user})

def chatting_page_view(request: HttpRequest) -> HttpResponse:

    return render(request, 'chatting page.html')