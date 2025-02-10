from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from python_blog import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', views.about, name="about"),
    path('posts/', include('python_blog.urls')),
    path('',  views.main, name="main"),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]