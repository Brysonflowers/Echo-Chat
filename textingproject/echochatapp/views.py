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
    users = User.objects.exclude(id=request.user.id) # Exclude current user
    return render(request, "index.html", {'users': users})


@login_required
def thecurrentchatviewer(request: HttpRequest, room_name: str) -> HttpResponse:
    chat_group = get_object_or_404(ChatGroup, name=room_name)
    messages = Message.objects.filter(group=chat_group).order_by('timestamp').all()[:10]
    chat_groups = ChatGroup.objects.all()
    return render(request, "chattextpage.html", {'room_name': room_name, 'messages': messages, 'chat_groups': chat_groups})

@login_required
def private_chat_room_view(request: HttpRequest, private_chat_id: str) -> HttpResponse:
    from django.db.models import Q
    from django.http import HttpResponseForbidden

    # private_chat_id will be in format like "user1_user2"
    user_ids = sorted([int(uid) for uid in private_chat_id.split('_')])
    user1 = get_object_or_404(User, id=user_ids[0])
    user2 = get_object_or_404(User, id=user_ids[1])

    # Ensure the current user is one of the participants
    if request.user not in [user1, user2]:
        return HttpResponseForbidden("You are not part of this private chat.")

    messages = Message.objects.filter(
        (Q(sender=user1, receiver=user2) | Q(sender=user2, receiver=user1)),
        group__isnull=True # Ensure it's a private message
    ).order_by('timestamp').all()[:10]

    return render(request, "private chat.html", {
        'private_chat_id': private_chat_id,
        'messages': messages,
        'other_user': user1 if request.user == user2 else user2 # For display purposes
    })

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

@login_required
def private_chats_view(request: HttpRequest) -> HttpResponse:
    users = User.objects.exclude(id=request.user.id) # Exclude current user
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