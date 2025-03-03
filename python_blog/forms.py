from django import forms
from django.forms import widgets

from python_blog.models import Post


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False)
    s_from = forms.CharField(max_length=100, required=False)


class PostForm(forms.ModelForm):
    model = Post
    fields = [
        "title",
        "content",
        "category",
    ]
    tag_string = forms.CharField(max_length=200, required=False)

    class Meta:
        model = Post
        fields = ["title", "content", "category"]
        widgets = {
            "category": widgets.Select(attrs={"class": "form-control"}),
        }