# blog/urls.py (Главная конфигурация URL)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('python_blog.urls')),  # Подключение маршрутов приложения
]