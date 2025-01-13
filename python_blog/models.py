from django.db import models
from django.contrib.auth.models import User
from slugify import slugify
from django.urls import reverse


class Menu(models.Model):
    """Модель для хранения пунктов меню сайта. Мне кажется что это не нужно, но я не уверен.
    
    Attributes:
        title (str): Название пункта меню, уникальное поле
        slug (str): URL-путь для пункта меню
    """
    title = models.CharField(max_length=100, unique=True, verbose_name='Название')
    slug = models.CharField(max_length=100, verbose_name="URL")

    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'


class Categories(models.Model):
    """Модель для хранения категорий постов.
    При сохранении автоматически генерирует slug из названия категории.
    
    Attributes:
        category_name (str): Название категории, уникальное поле
        slug (str): Автоматически генерируемый URL-путь категории
    """
    category_name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.category_name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("block:category_detali", args=[self.slug])
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Tags(models.Model):
    """Модель для хранения тегов постов.
    
    Attributes:
        name (str): Название тега, уникальное поле
    """
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Post(models.Model):
    """Модель для хранения постов блога.
    При сохранении автоматически генерирует slug из заголовка поста.
    
    Attributes:
        author (User): Автор поста, связь с моделью User
        title (str): Заголовок поста, уникальное поле
        slug (str): Автоматически генерируемый URL-путь поста
        content (str): Текст поста
        hashtags (ManyToManyField): Связь с моделью Tags, для выбора и хранения тегов
        views (int): Количество просмотров поста, пока просто числа
        likes (int): Количество лайков поста, пока просто числа
        category (Categories): Категория поста, связь с моделью Categories
        created_at (datetime): Дата создания поста
        updated_at (datetime): Дата последнего обновления поста
        image (ImageField): Изображение поста
        is_published (bool): Статус публикации поста
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = 'Автор')
    title = models.CharField(max_length=200, unique=True, verbose_name='Заголовок')
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField( verbose_name='Содержание')
    hashtags = models.ManyToManyField(Tags, blank=True)
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    likes = models.IntegerField(default=0, verbose_name='Лайки')
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='posts', verbose_name='Категория')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    image = models.ImageField(upload_to='media/posts/')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("block:post_detail", args=[self.slug])

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comments(models.Model):
    """Модель для хранения комментариев к постам.
    
    Attributes:
        author (User): Автор комментария, связь с моделью User
        content (str): Текст комментария
        post (Post): Пост к которому относится комментарий, связь с моделью Post
        created_at (datetime): Дата создания комментария
        updated_at (datetime): Дата последнего обновления комментария
        is_published (bool): Статус публикации комментария
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    content = models.TextField(max_length=500, verbose_name='Комментарий')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')

    def __str__(self):
        return f"Комментарий от {self.author} на пост '{self.post}'"

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'