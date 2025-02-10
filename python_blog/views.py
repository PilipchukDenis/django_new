from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from .models import Category, Post, Tag
from django.db.models import Count
from django.core.paginator import Paginator


def main(request):
    catalog_categories_url: str = reverse('blog:catalog_categories')
    catalog_tags_url: str = reverse('blog:catalog_tags')

    context = {
        "title": "Главная страница",
        "text": "Текст главной страницы",
        "user_status": "admin",
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
    posts= Post.objects.select_related('category', 'author').prefetch_related('tags').all()
    paginator = Paginator(posts, 3) # Показываем по 3 поста на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Блог',
        'posts': page_obj
    }
    return render(request, 'blog.html', context)

def post_detail(request, post_slug):
    post= Post.objects.get(slug=post_slug)
    context= {
        "title": post.title, 
        "post": post
    }
    return render(request, 'post_detail.html', context)

def catalog_categories(request):
    categories= Category.objects.all()
    paginator = Paginator(categories, 5) # Показываем по 5 категорий на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context= {
        "categories": page_obj, 
        "title": "Категории блога"
    }
    return render(request, "catalog_categories.html", context)

def category_detail(request, category_slug):
    category: dict[str, str] = Category.objects.get(slug=category_slug)
    posts= category.posts.all()
    paginator = Paginator(posts, 2) # Показываем по 2 поста на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={
        "title": f"Категория: {category.name}",
        "category": category,
        "posts": page_obj,
        "active_menu": "categories"
    }
    return render(request, "category_detail.html", context)


def catalog_tags(request):
    tags = Tag.objects.annotate(posts_count=Count('posts')).order_by('-posts_count')
    paginator = Paginator(tags, 3) # Показываем по 3 тега на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "title": "Теги блога",
        "tags": page_obj,
        "active_menu": "tags"
    }
    return render(request, "catalog_tags.html", context)

def tag_detail(request, tag_slug):
    tag = Tag.objects.get(slug=tag_slug)
    posts = tag.posts.all()
    paginator = Paginator(posts, 3) # Показываем по 3 поста на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "title": f"Тег: {tag.name}",
        "tag": tag,
        "posts": page_obj,
        "active_menu": "tags"
    }
    return render(request, "tag_detail.html", context)
