from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from .blog_data import dataset

CATEGORIES = [
    {"slug": "python", "name": "Python"},
    {"slug": "django", "name": "Django"},
    {"slug": "postgresql", "name": "PostgreSQL"},
    {"slug": "docker", "name": "Docker"},
    {"slug": "linux", "name": "Linux"},
]


def main(request):
    catalog_categories_url = reverse("blog:categories")
    catalog_tags_url = reverse("blog:tags")

    context = {
        "title": "Главная страница",
        "text": "Текст главной страницы",
        "user_status": "moderator",
    }
    return render(request, "main.html", context)


def about(request):
    context = {
        "title": "О компании",
        "text": "Мы - команда профессионалов в области веб-разработки",
    }
    return render(request, "about.html", context)


def catalog_posts(request):
    # Получаем все опубликованные посты
    posts = [post for post in dataset if post['is_published']]
    context = {
        'title': 'Блог',
        'posts': posts
    }
    return render(request, 'blog.html', context)

def post_detail(request, post_id):
    post = None  # Заглушка для одного поста (позже подключим базу данных)
    return render(request, 'post_detail.html', {'post': post})

def catalog_categories(request):
    links = []
    for category in CATEGORIES:
        url = reverse("blog:category_detail", args=[category["slug"]])
        links.append(f'<p><a href="{url}">{category["name"]}</a></p>')

    context = {
        "title": "Категории",
        "text": "Текст страницы с категориями",
        "categories": CATEGORIES,
    }
    return render(request, "catalog_categories.html", context)


def category_detail(request, category_slug):

    category = [cat for cat in CATEGORIES if cat["slug"] == category_slug][0]

    if category:
        name = category["name"]
    else:
        name = category_slug

    return HttpResponse(
        f"""
        <h1>Категория: {name}</h1>
        <p><a href="{reverse('blog:categories')}">Назад к категориям</a></p>
    """
    )


def catalog_tags(request):
    return HttpResponse("Каталог тегов")


def tag_detail(request, tag_slug):
    return HttpResponse(f"Страница тега {tag_slug}")
# Главная страница
def main_page(request):
    return render(request, 'main.html')  # Отправляем в шаблон main.html

# О проекте
def about_page(request):
    return render(request, 'about.html')  # Отправляем в шаблон about.html
def blog_page(request):
    posts = []  # Пока заглушка для списка постов
    return render(request, 'blog.html', {'posts': posts})  # Передаём в шаблон список постов