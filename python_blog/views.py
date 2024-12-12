from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.urls import reverse

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


def catalog_posts(request):
    return HttpResponse("Каталог постов")


def post_detail(request, post_slug):
    return HttpResponse(f"Страница поста {post_slug}")


def catalog_categories(request):
    links = []
    for category in CATEGORIES:
        url = reverse("blog:category_detail", args=[category["slug"]])
        links.append(f'<p><a href="{url}">{category["name"]}</a></p>')

    context  = {
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