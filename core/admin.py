from django.contrib import admin
from .models import Master, Service, Visit, Review
from django.db.models import Sum, Count, Q
from django.contrib import messages

# Функции-обработчики для массового изменения статусов отзывов


def make_published(modeladmin, request, queryset):
    """Установить статус 'Опубликован' для выбранных отзывов"""
    updated = queryset.update(status=0)
    modeladmin.message_user(
        request, f"{updated} отзывов успешно опубликовано", messages.SUCCESS
    )


make_published.short_description = "Опубликовать выбранные отзывы"


def mark_as_unverified(modeladmin, request, queryset):
    """Установить статус 'Не проверен' для выбранных отзывов"""
    updated = queryset.update(status=1)
    modeladmin.message_user(
        request, f"{updated} отзывов отмечено как непроверенные", messages.SUCCESS
    )


mark_as_unverified.short_description = "Отметить как непроверенные"


def approve_reviews(modeladmin, request, queryset):
    """Установить статус 'Одобрен' для выбранных отзывов"""
    updated = queryset.update(status=2)
    modeladmin.message_user(request, f"{updated} отзывов одобрено", messages.SUCCESS)


approve_reviews.short_description = "Одобрить выбранные отзывы"


def reject_reviews(modeladmin, request, queryset):
    """Установить статус 'Отклонен' для выбранных отзывов"""
    updated = queryset.update(status=3)
    modeladmin.message_user(request, f"{updated} отзывов отклонено", messages.SUCCESS)


reject_reviews.short_description = "Отклонить выбранные отзывы"


# Определяем кастомные фильтры
class PriceRangeFilter(admin.SimpleListFilter):
    # Заголовок фильтра в боковой панели
    title = "Ценовая категория"

    # Имя параметра в URL
    parameter_name = "price_range"

    def lookups(self, request, model_admin):
        # Определяем варианты для выбора в фильтре
        return (
            ("low", "До 1000₽"),
            ("medium", "1000₽ - 3000₽"),
            ("high", "Более 3000₽"),
        )

    def queryset(self, request, queryset):
        # Логика фильтрации
        if self.value() == "low":
            # Используем подзапрос для вычисления суммы цен услуг
            # Аннотируем каждую запись суммой цен всех выбранных услуг
            return queryset.annotate(total_price=Sum("services__price")).filter(
                total_price__lte=1000
            )

        if self.value() == "medium":
            return queryset.annotate(total_price=Sum("services__price")).filter(
                total_price__gt=1000, total_price__lte=3000
            )

        if self.value() == "high":
            return queryset.annotate(total_price=Sum("services__price")).filter(
                total_price__gt=3000
            )

        return queryset


class RegularClientsFilter(admin.SimpleListFilter):
    # Заголовок фильтра в боковой панели
    title = "Постоянные клиенты"

    # Имя параметра в URL
    parameter_name = "is_regular"

    def lookups(self, request, model_admin):
        # Определяем варианты для выбора в фильтре
        return (
            ("yes", "Да (3+ записи)"),
            ("no", "Нет (менее 3 записей)"),
        )

    def queryset(self, request, queryset):
        # Логика фильтрации
        if self.value() == "yes":
            # Получаем телефоны клиентов, у которых 3 и более записей
            regular_phones = (
                Visit.objects.values("phone")
                .annotate(visit_count=Count("id"))
                .filter(visit_count__gte=3)
                .values_list("phone", flat=True)
            )

            # Фильтруем записи по этим телефонам
            return queryset.filter(phone__in=regular_phones)

        if self.value() == "no":
            # Получаем телефоны клиентов с менее чем 3 записями
            non_regular_phones = (
                Visit.objects.values("phone")
                .annotate(visit_count=Count("id"))
                .filter(visit_count__lt=3)
                .values_list("phone", flat=True)
            )

            # Фильтруем записи по этим телефонам
            return queryset.filter(phone__in=non_regular_phones)

        return queryset


# Определяем классы инлайнов
class ReviewInline(admin.TabularInline):  # TabularInline отображает в виде таблицы
    model = Review
    extra = 0  # количество пустых форм для добавления
    readonly_fields = ("text", "rating", "created_at")
    can_delete = False  # запрет на удаление
    max_num = 10  # максимальное количество отзывов на странице
    ordering = ("-created_at",)


class VisitInline(admin.TabularInline):
    model = Visit
    extra = 0
    readonly_fields = ("created_at",)
    fields = ("name", "phone", "status", "created_at")
    max_num = 10  # максимальное количество записей на странице
    ordering = ("-created_at",)


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    # Отображаемые поля в списке записей (порядок учитывается)
    list_display = ("first_name", "last_name", "phone")

    # inlines - добавляем наши инлайны
    inlines = [VisitInline, ReviewInline]
    filter_horizontal = ("services",)  # улучшенный виджет для ManyToMany поля


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    # Отображаемые поля в списке записей (порядок учитывается)
    list_display = ("name", "price")
    # Поля которые будут учитываться в поиске
    search_fields = ("name", "description")
    # Кликабельные ссылки на поля
    list_display_links = ("name", "price")
    # Поля только на чтение
    # readonly_fields = ('description',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    # Эти поля будут закрыты на редактирование для ВСЕХ!
    readonly_fields = ("text", "rating", "master")
    # Поля которые будут учитываться в поиске
    search_fields = ("text", "name", "master")
    # Отображаемые столбцы в таблице
    list_display = ("name", "rating", "status", "created_at")
    # Сортировка по created_at сверху свежие
    ordering = ("-created_at",)
    # Сколько отзывов на странице?
    list_per_page = 10
    # Фильтры. По рейтингу, мастерам, статусу и дате
    list_filter = ("rating", "master", "status", "created_at")

    # Добавляем экшены для массового редактирования
    actions = [make_published, mark_as_unverified, approve_reviews, reject_reviews]


# Visit
@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):

    # Метод для кастомного столбца
    # Добавляем custom метод для отображения общей суммы
    def get_total_price(self, obj):
        # Вычисляем сумму всех услуг для данного визита
        total = obj.services.aggregate(total=Sum("price"))["total"]
        # Проверяем, что сумма не None (если услуг нет)
        if total:
            # Форматируем с символом рубля
            return f"{total:.2f} ₽"
        return "0.00 ₽"

    # Задаем название столбца в админке
    get_total_price.short_description = "Общая сумма"
    # Включаем возможность сортировки по этому полю
    get_total_price.admin_order_field = "services__price"

    # Поля которые будут учитываться в поиске
    search_fields = ("phone", "name", "comment", "services__name")
    # Отображаемые столбцы в таблице
    list_display = (
        "name",
        "phone",
        "created_at",
        "status",
        "master",
        "get_total_price",
    )
    # Сортировка по дате
    ordering = ("created_at", "master")
    # Фильтры. По услуге, мастеру, клиенту и дате
    list_filter = ("master", "created_at", PriceRangeFilter, RegularClientsFilter)
    filter_horizontal = ("services",)
    # filter_vertical = ('services',)

    # Делаем поле status редактируемым прямо в списке
    list_editable = ("status",)
