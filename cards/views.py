from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render
from .models import Card
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page



info = {
    "users_count": 100500,
    "cards_count": 200600,
    "menu": [
        {"title": "Главная",
         "url": "/",
         "url_name": "index"},
        {"title": "О проекте",
         "url": "/about/",
         "url_name": "about"},
        {"title": "Каталог",
         "url": "/cards/catalog/",
         "url_name": "catalog"},
    ],
}


def index(request):
    """Функция для отображения главной страницы
    будет возвращать рендер шаблона root/templates/main.html"""
    return render(request, "main.html", info)


def about(request):
    """Функция для отображения страницы "О проекте"
    будет возвращать рендер шаблона /root/templates/about.html"""
    return render(request, 'about.html', info)


@cache_page(60 * 15)  # Кэширует на 15 минут
def catalog(request):
    """
    Функция для отображения каталога карточек с возможностью сортировки.
    Параметры GET запроса:
    - sort: ключ для сортировки (допустимые значения: 'upload_date', 'views', 'adds').
    - order: порядок сортировки ('asc' для возрастания, 'desc' для убывания; по умолчанию 'desc').
    """
    # Считываем параметры из GET запроса
    sort = request.GET.get('sort', 'UploadDate')  # по умолчанию сортируем по дате загрузки
    order = request.GET.get('order', 'desc')  # по умолчанию используем убывающий порядок

    # Сопоставляем параметр сортировки с полями модели
    valid_sort_fields = {'UploadDate', 'views', 'favorites'}  # Исправил 'adds' на 'favorites', предполагая, что это опечатка
    if sort not in valid_sort_fields:
        sort = 'UploadDate'  # Возвращаемся к сортировке по умолчанию, если передан неверный ключ сортировки

    # Обрабатываем порядок сортировки
    if order == 'asc':
        order_by = sort
    else:
        order_by = f'-{sort}'

    # Получаем отсортированные карточки через ЖАДНУЮ ЗАГРУЗКУ
    cards = Card.objects.prefetch_related('tags').order_by(order_by)

    context = {
        'cards': cards,
        'cards_count': len(cards),
        'sort': sort,  # Добавлено для возможности отображения текущей сортировки в шаблоне
        'order': order,  # Добавлено для возможности отображения текущего порядка в шаблоне
        'menu': info['menu'],  # Добавлено для отображения меню на странице
    }
    return render(request, 'cards/catalog.html', context)



def get_categories(request):
    """
    Возвращает все категории для представления в каталоге
    """
    # Проверка работы базового шаблона
    return render(request, 'base.html', info)


def get_cards_by_category(request, slug):
    """
    Возвращает карточки по категории для представления в каталоге
    """
    return HttpResponse(f'Cards by category {slug}')

@cache_page(60 * 15)  # Кэширует на 15 минут
def get_cards_by_tag(request, tag_id):
    """
    Возвращает карточки по тегу для представления в каталоге
    Мы используем многие-ко-многим, получая все карточки, которые связаны с тегом
    Временно, мы будем использовать шаблон каталога
    """
    # cards = Card.objects.filter(tags=tag_id)

    # Жадная загрузка
    cards = Card.objects.filter(tags=tag_id).prefetch_related('tags')
    context = {
        'cards': cards,
        'cards_count': cards.count(),
        'menu': info['menu'],
    }
    return render(request, 'cards/catalog.html', context)


def get_detail_card_by_id(request, card_id):
    card_obj = get_object_or_404(Card.objects.prefetch_related('tags'), pk=card_id)
    
    # Обновление счетчика просмотров
    Card.objects.filter(pk=card_id).update(views=F('views') + 1)
    
    card = {
        "card": card_obj,
        "menu": info["menu"],
    }

    return render(request, 'cards/card_detail.html', card, status=200)
