from django.urls import path
from .views import *


urlpatterns = [
    path("sign_up/", SignUpView.as_view(), name="signup"),
    path("create_group/", create_group, name="create_group"),
]