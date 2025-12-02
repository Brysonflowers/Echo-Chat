from django.urls import path, include
from .views import *

urlpatterns = [
    path("sign_up/", SignUpView.as_view(), name="signup"),
    # path("create_group/", create_group, name="create_group"),
    path('chat/<str:room_name>/', thecurrentchatviewer, name='chat'),
    path('private_chat/<str:private_chat_id>/', private_chat_room_view, name='private_chat_room'),
    path('private-chats', private_chats_view, name = 'private_chats'),
    path('chatting-page', chatting_page_view, name='chatting_page'),
    # path('search/', search_view, name='search'),
    path('create-group-chat/', CreateGroupChatView.as_view(), name='create_group_chat'),
    path('group/<int:group_id>/', group_chat_view, name='group_chat'),
    path("accounts/", include('django.contrib.auth.urls')),
]