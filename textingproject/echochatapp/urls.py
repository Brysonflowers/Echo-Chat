SignUpView.as_view(), name="signup"),
    path("create_group/", SignUpView.as_view(), name="signup"),
    path("create_group/", create_group, name="create_group"),
    path('chat/<str:room_name>/', thecurrentchatviewer, name='chat'),
    path('private chats', private_chats_view, name = 'private_chats'),
    path('chatting page', chatting_page_view, name='chatting_page'),
    path("accounts/", include('django.contrib.auth.urls')),
]