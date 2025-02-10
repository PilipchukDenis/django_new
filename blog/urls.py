from django.contrib import admin
from django.urls import path, include
from python_blog.views import main, about

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', about, name='about'),
    path('', main, name='main'),

    # Подключаем python_blog.urls
    path('posts/', include('python_blog.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]