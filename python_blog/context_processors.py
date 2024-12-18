"""
Контекстный процессор передающий меню в каждый из шаблонов Джанго!
Не забудьте подключить это в в settings.py -> TEMPLATES -> context_processors
'python_blog.context_processors.menu_items', 
"""

MENU_ITEMS = [
    {"title": "Главная", "url_name": "main"},
    {"title": "Все посты", "url_name": "blog:posts"},
    {"title": "Категории", "url_name": "blog:categories"},
    {"title": "Теги", "url_name": "blog:tags"},
]



def menu_items(request):
    return {
        'menu_items': MENU_ITEMS
    }