from django.contrib import admin
from django.urls import path, include
from echochatapp.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', index, name = 'home'),
    path("sign_up/", SignUpView.as_view(), name="signup"),
    path("create_group/", create_group, name="create_group"),
    path('chat',thecurrentchatviewer,name='chat'),
    path('private chats', private_chats_view, name = 'private_chats'),
    path('chatting page', chatting_page_view, name='chatting_page'),
    path("accounts/", include('django.contrib.auth.urls')),
]