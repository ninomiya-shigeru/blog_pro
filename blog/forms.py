from django import forms
from .models import Message
from django.contrib.auth.models import User


# 投稿フォーム
class PostForm(forms.Form):
    content = forms.CharField(max_length=2000,
             widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10}))
    photo1 = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        label='画像1'
    )

