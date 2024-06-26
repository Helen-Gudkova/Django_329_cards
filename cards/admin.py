"""
python manage.py createsuperuser - создание суперпользователя
Есть 2 варианта регистрации
admin.site.register() или @admin.register()
@admin.display() - декоратор для отображения дополнительных полей
параметры декоратора: description - название поля, ordering - сортировка (реальное поле из модели)
"""

from django.contrib import admin

from .models import Card, Category, Tag, CardTags


class CheckStatusFilter(admin.SimpleListFilter):
    title = 'Статус проверки' # Название фильтра, которое будет отображаться в админке
    parameter_name = 'check_status' # Имя параметра, который будет передаваться в URL

    def lookups(self, request, model_admin):
        """
        Метод для определения значений фильтрации
        Возвращает кортежи с двумя значениями: значение и отображаемое имя
        :param request:
        :param model_admin:
        :return:
        """
        return (
            ('UNCHECKED', 'Не проверено'),
            ('CHECKED', 'Проверено'),
        )

    def queryset(self, request, queryset):
        """
        Метод для фильтрации
        self.value() - получение значения фильтра
        :param request:
        :param queryset:
        :return:
        """
        if self.value() == 'UNCHECKED':
            return queryset.filter(check_status=0)
        if self.value() == 'CHECKED':
            return queryset.filter(check_status=1)

class CardCodeFilter(admin.SimpleListFilter):
    title = 'Наличие кода'
    parameter_name = 'has_code'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Да'),
            ('no', 'Нет'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(Answer__contains='```')
        elif self.value() == 'no':
            return queryset.exclude(Answer__contains='```')
            
@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('get_questions', 'check_status', 'UploadDate', 'category_name', 'tags_list', 'brief_info')
    list_display_links = ('get_questions',)
    list_filter = ('Category', CheckStatusFilter)
    search_fields = ('Question', 'Category__name', 'Answer', 'tags__name')
    ordering = ('-UploadDate', 'Question')
    list_per_page = 20
    actions = ['mark_as_checked', 'mark_as_unchecked']
    fields = ('Question', 'Answer', 'Category_id') 
    readonly_fields = ('tags',)  # Использовать readonly_fields вместо fields
    #filter_vertical = ('tags',)  # Добавьте filter_vertical для вертикального отображения списка тегов

    def tags_list(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    tags_list.short_description = 'Tags'

    def check_status(self, obj):
        # Логика для определения статуса проверки
        return obj.check_status
    check_status.short_description = 'Check Status'


    # list_editable = ('category_name',) # Редактируемое поле
    # Добавляем метод для отображения названия категории
    @admin.display(description="Категория", ordering='Category_id__name')
    def category_name(self, obj):
        return obj.Category_id.Name if obj.Category_id else 'Без категории'
    # Дополнительный метод для отображения списка тегов
    @admin.display(description="Теги", ordering='tags__name')
    def tags_list(self, obj):
        return " | ".join([tag.Name for tag in obj.tags.all()])

    # Определение метода для отображения краткой информации о карточке
    # ordering по полю answer, так как точного поля для сортировки по краткому описанию нет
    @admin.display(description="Краткое описание", ordering='answer')
    def brief_info(self, card):
        # Определяем длину ответа
        length = len(card.Answer)
        # Проверяем наличие кода
        has_code = 'Да' if '```' in card.Answer else 'Нет'
        return f"Длина ответа: {length}, Код: {has_code}"

    # Дополнительный метод для отображения вопросов
    def get_questions(self, obj):
        row_question = obj.Question
        result_question = row_question.replace('##', '').replace('`', '').replace('**', '').replace('*', '')
        return result_question

    get_questions.short_description = 'Вопрос'

    @admin.action(description='Отметить как проверенные')
    def mark_as_checked(self, request, queryset):
        queryset.update(check_status=True)


    @admin.action(description='Отметить как непроверенные')
    def mark_as_unchecked(self, request, queryset):
        queryset.update(check_status=False)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(CardTags)
class CardTagsAdmin(admin.ModelAdmin):
    # Отображаемые поля
    list_display = ('card', 'tag')
