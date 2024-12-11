
# views.py
from django.http import HttpResponse, Http404
from django.urls import reverse

# Константы данных
CATEGORIES = [
    {'slug': 'python', 'name': 'Python'},
    {'slug': 'django', 'name': 'Django'},
    {'slug': 'postgresql', 'name': 'PostgreSQL'},
    {'slug': 'docker', 'name': 'Docker'},
    {'slug': 'linux', 'name': 'Linux'},
]

# Главная страница
def main(request):
    links = [
        f'<a href="{reverse("catalog_posts")}">Каталог постов</a>',
        f'<a href="{reverse("catalog_categories")}">Каталог категорий</a>',
        f'<a href="{reverse("catalog_tags")}">Каталог тегов</a>',
    ]
    return HttpResponse('<br>'.join(links))

# Каталог постов
def catalog_posts(request):
    return HttpResponse('Здесь будут отображаться все доступные посты.')

# Каталог категорий
def catalog_categories(request):
    html = "<ul>"
    for category in CATEGORIES:
        html += f'<li><a href="{reverse("category_detail", args=[category["slug"]])}">{category["name"]}</a></li>'
    html += "</ul>"
    return HttpResponse(html)

# Детальная информация о категории
def category_detail(request, category_slug):
    category = next((cat for cat in CATEGORIES if cat['slug'] == category_slug), None)
    if category is None:
        raise Http404("Категория не найдена")
    return HttpResponse(f'Детальная информация о категории: {category["name"]}')

# Каталог тегов
def catalog_tags(request):
    # Фиктивные данные о тегах
    TAGS = [
        {'slug': 'web', 'name': 'Web'},
        {'slug': 'backend', 'name': 'Backend'},
        {'slug': 'frontend', 'name': 'Frontend'},
    ]
    html = "<ul>"
    for tag in TAGS:
        html += f'<li><a href="{reverse("tag_detail", args=[tag["slug"]])}">{tag["name"]}</a></li>'
    html += "</ul>"
    return HttpResponse(html)

# Детальная информация о теге
def tag_detail(request, tag_slug):
    # Фиктивные данные о тегах
    TAGS = [
        {'slug': 'web', 'name': 'Web'},
        {'slug': 'backend', 'name': 'Backend'},
        {'slug': 'frontend', 'name': 'Frontend'},
    ]
    tag = next((tag for tag in TAGS if tag['slug'] == tag_slug), None)
    if tag is None:
        raise Http404("Тег не найден")
    return HttpResponse(f'Детальная информация о теге: {tag["name"]}')

# Детальная информация о посте
def post_detail(request, post_id):
    return HttpResponse(f'Детальная информация о посте с ID: {post_id}')

