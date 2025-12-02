from django import forms
from .models import *

class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = ChatGroup
        fields = ['name']

class SearchUserForm(forms.Form):
    name = forms.CharField(max_length=20)

class SendChatRequestForm(forms.Form):
    chat_request = forms.BooleanField()

# Dani added this new form for creating group chats we can delete it if not needed
class CreateGroupChatForm(forms.ModelForm):
        members = forms.ModelMultipleChoiceField(
            queryset=User.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=True
        )

        class Meta:
            model = ChatGroup
            fields = ['name', 'members']


class GroupMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Type your message...', 'class': 'form-control'})
        }
    name = forms.CharField(max_length=20)
