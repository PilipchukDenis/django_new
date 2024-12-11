from django.contrib import admin
from django.urls import path
from python_blog.views import main

urlpatterns: list[any] = [
    path('admin/', admin.site.urls),
    path('<str:name>/', main),
]
