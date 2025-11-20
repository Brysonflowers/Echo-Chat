from django import forms
from .models import ChatGroup

class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = ChatGroup
        fields = ['name']

class SearchUserForm(forms.Form):
    name = forms.CharField(max_length=20)