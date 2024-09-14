from django import forms
from django.utils import timezone

from .models import Comment, Post


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                },
                format="%Y-%m-%dT%H:%M",
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pub_date'].initial = timezone.now()


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
