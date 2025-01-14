from django.db import models
from django.contrib.auth import get_user_model
from unidecode import unidecode
from django.utils.text import slugify
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    data = models.JSONField(blank=True, null=True, default=list)
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
            print(self.slug)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'post_slug': self.slug})