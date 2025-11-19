from django import forms
from .models import ChatGroup

class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = ChatGroup
        fields = ['name']
