from django.contrib import admin
from .models import Categories, Post, Comments, Tags

class TagsInline(admin.TabularInline):
    """Встроенная админ-форма для отображения тегов в постах.
    Позволяет добавлять и редактировать теги непосредственно при редактировании поста.
    
    Attributes:
        model: Промежуточная модель для связи Post и Tags
        extra: Количество дополнительных пустых форм для добавления тегов
    """
    model = Post.hashtags.through
    extra = 1


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели Categories.
    
    Attributes:
        list_display: Отображаемые поля в списке категорий (id, название, slug)
        exclude: Исключенные поля из формы редактирования (slug генерируется автоматически)
    """
    list_display = ('id', 'category_name', 'slug')
    exclude = ('slug',)


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели Comments.
    
    Attributes:
        list_display: Отображаемые поля в списке комментариев (id, автор, пост, дата создания)
    """
    list_display = ('id', 'author', 'post', 'created_at')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели Post.
    Включает встроенную форму для управления тегами.
    
    Attributes:
        list_display: Отображаемые поля в списке постов (id, заголовок, slug, автор, дата создания)
        inlines: Встроенные формы (TagsInline для управления тегами)
        exclude: Исключенные поля из формы редактирования (slug генерируется автоматически, hashtags управляются через inline-форму)
    """
    list_display = ('id', 'title', 'is_published', 'slug', 'author', 'created_at')
    inlines = [TagsInline]
    exclude = ('slug', 'hashtags')


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели Tags.
    
    Attributes:
        list_display: Отображаемые поля в списке тегов (только название)
    """
    list_display = ['name']