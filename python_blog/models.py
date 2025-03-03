from django.db import models
from unidecode import unidecode
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, blank=True, verbose_name='URL')

    def __str__(self):
        return str(self.name)

class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, blank=True, verbose_name='URL')

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание", null=True)
    slug = models.SlugField(unique=True, blank=True, verbose_name="URL")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="posts",
        null=True,
        blank=True,
        verbose_name="Категория",
    )
    tags = models.ManyToManyField(
        Tag, related_name="posts", blank=True, verbose_name="Теги"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    views = models.IntegerField(default=0, verbose_name="Просмотры")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
            print(self.slug)
        super().save(*args, **kwargs)

    def str(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"post_slug": self.slug})  