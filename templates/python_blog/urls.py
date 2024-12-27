# python_blog\urls.py Django APP python_blog
from django.contrib import admin
from django.urls import path
from python_blog.views import catalog_posts, post_detail, catalog_categories, category_detail, catalog_tags, tag_detail

app_name = 'blog'


# Общий префикс posts/
urlpatterns = [
    # Каталог  постов posts/
    path('', catalog_posts, name='posts'),
    
    # Категории
    # Категории posts/categories/
    # Категории posts/categories/python/
    path('categories/', catalog_categories, name='categories'),
    path('categories/<slug:category_slug>/', category_detail, name='category_detail'),
    
    # Теги posts/tags/
    # Теги posts/tags/python/
    path('tags/', catalog_tags, name='tags'),
    path('tags/<slug:tag_slug>/', tag_detail, name='tag_detail'),
    
    # Посты posts/
    path('<slug:post_slug>/', post_detail, name='post_detail'),
]