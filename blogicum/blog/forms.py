from django import forms
from .models import Post, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
import re


User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if not re.match(r'^[\w-]+$', username):
            raise forms.ValidationError(
                "Никнейм может содержать только буквы, цифры, подчеркивания и дефисы."
            )
        return username


class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        exclude = ('author',)


class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ('text',)
