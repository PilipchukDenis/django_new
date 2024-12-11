
# python_blog/urls.py
from django.urls import path
from .views import (
    main, catalog_posts, catalog_categories,
    category_detail, catalog_tags, tag_detail, post_detail
)

app_name = 'python_blog'

urlpatterns = [
    path('', main, name='main'),
    path('posts/', catalog_posts, name='catalog_posts'),
    path('categories/', catalog_categories, name='catalog_categories'),
    path('categories/<slug:category_slug>/', category_detail, name='category_detail'),
    path('tags/', catalog_tags, name='catalog_tags'),
    path('tags/<slug:tag_slug>/', tag_detail, name='tag_detail'),
    path('<int:post_id>/', post_detail, name='post_detail'),
]

