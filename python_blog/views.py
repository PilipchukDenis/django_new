from django.http import HttpResponse, Http404
from django.urls import reverse

# Данные для категорий
CATEGORIES = [
    {'slug': 'python', 'name': 'Python'},
    {'slug': 'django', 'name': 'Django'},
    {'slug': 'postgresql', 'name': 'PostgreSQL'},
    {'slug': 'docker', 'name': 'Docker'},
    {'slug': 'linux', 'name': 'Linux'},
]

TAGS = [
    {'slug': 'web', 'name': 'Web'},
    {'slug': 'backend', 'name': 'Backend'},
    {'slug': 'frontend', 'name': 'Frontend'},
]

# Главная страница
def main(request):
    links = [
        f'<a href="{reverse("python_blog:catalog_posts")}">Каталог постов</a>',
        f'<a href="{reverse("python_blog:catalog_categories")}">Каталог категорий</a>',
        f'<a href="{reverse("python_blog:catalog_tags")}">Каталог тегов</a>',
    ]
    return HttpResponse('<br>'.join(links))


def catalog_posts(request):
    return HttpResponse("Здесь будет отображаться список всех постов в блоге.")


def catalog_categories(request):
    html = "<ul>"
    for category in CATEGORIES:
        html += f'<li><a href="{reverse("python_blog:category_detail", args=[category["slug"]])}">{category["name"]}</a></li>'
    html += "</ul>"
    return HttpResponse(html)


def category_detail(request, category_slug):
    category = next((cat for cat in CATEGORIES if cat['slug'] == category_slug), None)
    if category is None:
        raise Http404("Категория не найдена.")
    return HttpResponse(f'Детальная информация: {category["name"]}.')


def catalog_tags(request):
    html = "<ul>"
    for tag in TAGS:
        html += f'<li><a href="{reverse("python_blog:tag_detail", args=[tag["slug"]])}">{tag["name"]}</a></li>'
    html += "</ul>"
    return HttpResponse(html)


def tag_detail(request, tag_slug):
    tag = next((t for t in TAGS if t['slug'] == tag_slug), None)
    if tag is None:
        raise Http404("Тег не найден.")
    return HttpResponse(f'Детальная информация: {tag["name"]}.')

 

def post_detail(request, post_id):
    return HttpResponse(f'Детальная информация о посте с ID: {post_id}.')

