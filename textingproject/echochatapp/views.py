from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest
from django.http import HttpResponse
from .models import *
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
    ).order_by('timestamp').all()

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
    sender_user = User.objects.get(id=request.user.id)
    empty_dict = {}
    try:
        extra_info = PrivateChatRequest.objects.filter(sender_name = sender_user)
        extra_info[0] # extra_info indexed to check if is has info or is an empty query set, will cause an error if no info.
    except:
        extra_info = 'No Chat Requests'
    user = 'no name form'
    
    if request.POST != empty_dict:
        try:
            request.POST['Cancel Request']
            specific_user = PrivateChatRequest.objects.get(receiver_name = request.POST['Get User'])
            specific_user.delete()
            return redirect(request.path)
        except:
            try:
                user = request.POST['name']
                try:
                    user = users.get(username = user)
                except:
                    user = 'none with that name'
            except:
                user = 'sent chat request'
                sender_user = User.objects.get(id=request.user.id)
                PrivateChatRequest.objects.create(sender_name = sender_user, receiver_name = request.POST['user'], chat_request = request.POST['Chat Request'])
                return redirect(request.path)

    return render(request, 'private chat.html', {'users': users, 'name_form': SearchUserForm(), 'user': user, 'test': request, 'extra_info': extra_info, 'sender_user': sender_user},)

def chatting_page_view(request: HttpRequest) -> HttpResponse:

    return render(request, 'chatting page.html')

# def search_view(request: HttpRequest) -> HttpResponse:

#     return render(request, 'search.html')

# Dani added this new view for creating group chats we can delete it if not needed
class CreateGroupChatView(CreateView):
    model = ChatGroup
    form_class = CreateGroupChatForm
    template_name = 'create-group.html'
    success_url = reverse_lazy('create_group_chat')

    def form_valid(self, form):
        group = form.save(commit=False)
        group.owner = self.request.user
        group.save()
        form.save_m2m()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = ChatGroup.objects.all()
        return context

@login_required
def group_chat_view(request, group_id):
    group = get_object_or_404(ChatGroup, id=group_id)
    messages = group.messages.order_by('timestamp')  

    if request.method == "POST":
        form = GroupMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.group = group
            message.save()
            return redirect('group_chat', group_id=group.id)
    else:
        form = GroupMessageForm()

    return render(request, 'group_chat.html', {'group': group, 'messages': messages, 'form': form})


