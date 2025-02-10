from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode
# Функция get_userr_model() возвращает модель пользователя, которая используется по умолчанию в проекте.
from django.contrib.auth import get_user_model


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name="Заголовок")
    slug = models.SlugField(max_length=250, unique=True, verbose_name="Слаг", blank=True, null=True)
    content = models.TextField(verbose_name="Контент")
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Автор", related_name="posts", default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    views = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")
    # Категория - внешний ключ
    category = models.ForeignKey(
        "Category", # Ссылка на модель Category
        on_delete=models.SET_NULL, # При удалении категории, установить значение NULL
        blank=True, # Не требуем в формах заполнения
        null=True, # Разрешаем значение NULL в базе данных
        related_name="posts", # Имя обратной связи
        default=None, # Значение по умолчанию NULL
        verbose_name="Категория",
    )
    tags = models.ManyToManyField("Tag", related_name="posts", blank=True, verbose_name="Теги")

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-created_at"]

class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(max_length=250, unique=True, verbose_name="Слаг")
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("blog:tag_detail", args=[self.slug])
    
    
    def save(self , *args, **kwargs):
        self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["name"]

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Слаг")
    description = models.TextField(blank=True, null=True, default="Без описания", verbose_name="Описание")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Метод возвращает абсолютный URL для объекта Category
        В админке Django, при создании или редактировании категории, будет ссылка "Посмотреть на сайте". В шаблонах тоже удобно вызвать его.
        """
        return reverse("blog:category_detail", args=[self.slug])

    def save(self, *args, **kwargs):
        """
        Служебный метод для сохранения объекта в базу данных.
        Мы расширяем его, чтобы изменить логику сохранения объекта.
        """
        self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    class Meta:
        """
        Специальный вложенный  класс для настроек модели.
        """
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]





# PRACTICE - Работа с моделью Post
"""
1. Создать новый пост
post = Post(title="Django для чайников", content="Django очень легкий фреймворк, и у него пологая кривая входа...") 
post.save()

INSERT INTO "python_blog_post" ("title", "content", "created_at", "updated_at", "category")
VALUES ('Django для чайников', 'Django очень легкий фреймворк, и у него пологая кривая входа...', '2024-12-23 17:31:02.040654', '2024-12-23 17:31:02.040654', NULL) RETURNING "python_blog_post"."id"
Execution time: 0.000996s [Database: default]


post_1 = post

post_2 = Post(title="Базы данных для продавцов котиков", content="Теперь вы сможете каждого котика сохранить в базе данных")

Django ORM ленива.
Все запросы по умолчанию выполняются в ленивом режиме.
Допустим при сохранении, запрос будет выполнен только при вызове метода save()

При чтении, запрос выполнен при обращении к результату запроса

2. Получить все посты

posts = Post.objects.all()
posts = <QuerySet [<Post: Post object (1)>, <Post: Post object (2)>]>

Что такое QuerySet?
QuerySet - это набор объектов, которые мы получили из базы данных.
Мы можем использовать QuerySet для фильтрации, сортировки, группировки и других операций над объектами.

post_1 = post[0]
post_1

post_1.title
post_1.content
post_1.created_at

post_1.content = "Django не очень легкий фреймворк, но у него кривая входа..."
post_1.save()

post_3 = Post(title="Тестовый пост", content="Тестовый пост")

#  Делаем операцию удаления
post_3.delete()

3. Получить пост по id
post_1 = Post.objects.get(id=1) # id - поле модели id - это поле, которое автоматически генерируется Django
post_1 = Post.objects.get(pk=1) # pk - primary key - первичный ключ

4. Получим все посты и сортируем их по полю created_at от новых к старым
posts = Post.objects.all().order_by("-created_at")

5. Используя filter получим посты, где категория NULL
posts = Post.objects.filter(category=None)
Применим к полученному QuerySet сортировку
posts = posts.order_by("-created_at")
"""

# PRACTICE - Работа с моделью Category

"""
0. Запускаем shell  plus --print-sql
python manage.py shell_plus --print-sql

1. Создать новую категорию
category_1 = Category(name="Django", slug="django").save()
category_2 = Category(name="Python", slug="python").save()
category_3 = Category(name="Postgresql", slug="postgresql").save()
category_4 = Category(name="Docker", slug="docker").save()
category_5 = Category(name="Linux", slug="linux").save()


2. Получим все посты
posts = Post.objects.all()


3. Возьмем первый пост
post_1 = posts[0]

django_category = Category.objects.get(name="Django")

4. post_1 - хочу присвоить категорию django_category
post_1.category = django_category
post_1.save()

post_1 - это объект, который мы получили из базы данных.
post_1.title - это поле title у объекта post_1
post_1.category - экземпляр объекта Category, который мы присвоили объекту post_1

post_1.category.name - Django

# Обратное связывание. Мы обозначили relaated_name="posts" в модели Post

# Получим все посты по объекту категории
category = Category.objects.get(name="Django")
django_posts = category.posts.all()

# Если бы не было relaated_name="posts"

category = Category.objects.get(name="Django")
django_posts = Post.objects.filter(category=category)
# или

django_posts = Post.objects.filter(category__name="Django")



#################################  После обновления модели Category  ###################################################

Пробуем создать категорию (Убедимся, что кирилица не обрабатывается!!!)

category_6 = Category(name="Linux Аврора").save()
category_7 = Category(name="Добрый добрый JS").save()

category_8 = Category(name="Постгра").save()
category_9 = Category(name="Оракл БД").save()


####################################  Создание суперпользователя  #######################################################


"""

# PRACTICE Правктика с многие ко многим и Shell plus

"""
0. Запускаем shell  plus --print-sql
python manage.py shell_plus --print-sql

1. Создадим еще пару новых постов

post1 = Post.objects.create(title="Django ORM", content="Изучаем Django ORM")
post2 = Post.objects.create(title="Python Basic", content="Основы Python")

# Создадим пару тегов
tag1 = Tag.objects.create(name="Python")
tag2 = Tag.objects.create(name="Django")

# Добавим теги к постам
post1.tags.add(tag1, tag2) # Первому посту добавим оба тега
post2.tags.add(tag1) # Второму посту добавим только тег Python

# Получим пост со всеми его тегами
post_1 = Post.objects.get(id=1)

# Получим теги
post1.tags - Получим manager для связи многие ко многим
Мы можем вызвать его методы и получить все теги, связанные с этим постом
post1.tags.all() - кверисет

# Посчитаем количество тегов у поста
post1.tags.count()

# Получим теги, у которых есть py в имени
post1.tags.filter(name__icontains="py")

name - поле модели Tag
__icontains - фильтр по подстроке

# Посчитаем количество постов у тега tag1

posts_count = tag1.posts.count()

# Получим все посты, у которых есть тег tag1
post_with_tag1 = tag1.posts.all()

# Удалим тег tag2 у поста post1
post1.tags.remove(tag2)

# Обновим данные в переменной post_1
post_1.refresh_from_db()
"""