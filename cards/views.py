"""
index - возвращает главную страницу - шаблон /templates/cards/main.html
about - возвращает страницу "О проекте" - шаблон /templates/cards/about.html
catalog - возвращает страницу "Каталог" - шаблон /templates/cards/catalog.html


get_categories - возвращает все категории для представления в каталоге
get_cards_by_category - возвращает карточки по категории для представления в каталоге
get_cards_by_tag - возвращает карточки по тегу для представления в каталоге
get_detail_card_by_id - возвращает детальную информацию по карточке для представления

render(запрос, шаблон, контекст=None)
    Возвращает объект HttpResponse с отрендеренным шаблоном шаблон и контекстом контекст.
    Если контекст не передан, используется пустой словарь.
"""

from django.http import HttpResponse
from django.shortcuts import render
from django.template.context_processors import request
from django.shortcuts import render, get_object_or_404
from .models import Card, Tag
from .models import Card, CardTags

import json

"""
Информация в шаблоны будет браться из базы данных
Но пока, мы сделаем переменные, куда будем записывать информацию, которая пойдет в 
контекст шаблона
"""
# Пример данных для карточек
cards_dataset = [
    {
        "question": "Что такое PEP 8?",
        "answer": "PEP 8 — стандарт написания кода на Python.",
        "category": "Стандарты кода",
        "tags": ["PEP 8", "стиль", "форматирование"],
        "id_author": 1,
        "id_card": 1,
        "upload_date": "2023-01-15",
        "views_count": 100,
        "favorites_count": 25
    },
    {   "question": "Как объявить список в Python?",
        "answer": "С помощью квадратных скобок: lst = []",
        "category": "Основы",
        "tags": ["списки", "основы"],
        "id_author": 2,
        "id_card": 2,
        "upload_date": "2023-01-20",
        "views_count": 150,
        "favorites_count": 30
    },
    {
        "question": "Что делает метод .append()?",
        "answer": "Добавляет элемент в конец списка.",
        "category": "Списки",
        "tags": ["списки", "методы"],
        "id_author": 2,
        "id_card": 3,
        "upload_date": "2023-02-05",
        "views_count": 75,
        "favorites_count": 20
    },
    {
        "question": "Какие типы данных в Python иммутабельные?",
        "answer": "Строки, числа, кортежи.",
        "category": "Типы данных",
        "tags": ["типы данных", "иммутабельность"],
        "id_author": 1,
        "id_card": 4,
        "upload_date": "2023-02-10",
        "views_count": 90,
        "favorites_count": 22
    },
    {
        "question": "Как создать виртуальное окружение в Python?",
        "answer": "С помощью команды: python -m venv myenv",
        "category": "Виртуальные окружения",
        "tags": ["venv", "окружение"],
        "id_author": 2,
        "id_card": 5,
        "upload_date": "2023-03-01",
        "views_count": 120,
        "favorites_count": 40
}
]

info = {
    "users_count": 100500,
    "cards_count": 200600,
    "menu": [
        {"title": "Главная", "url": "/", "url_name": "index"},
        {"title": "О проекте", "url": "/about/", "url_name": "about"},
        {"title": "Каталог", "url": "/cards/catalog/", "url_name": "catalog"},
    ],
    "cards": cards_dataset
}


# Ваше представление main_page, где вы передаете данные о 5 карточках в шаблон

def index(request):
    return render(request, 'main.html',info)

def about(request):
    context = {
        "user_count": info["users_count"],
    }
    return render(request, 'about.html', context)


def catalog(request):
    sort = request.GET.get('sort', 'upload_date')
    sort_options = {
        'upload_date': '-UploadDate',
        'views': '-Views',
        'favorites': '-Favorites',
    }
    order = request.GET.get('order', 'desc')

    card_list = Card.objects.order_by(sort_options[sort])
    if order == 'asc':
        card_list = card_list.reverse()

    context = {
        'card_list': card_list,
        'current_sort': sort,
        'current_order': order
    }
    return render(request, 'catalog.html', context)


def card_detail(request, card_id):
    card = get_object_or_404(Card, card_id=card_id)
    return render(request, 'card_detail.html', {'card': card})


def get_cards_by_tag(request, tag_id):
    tag = get_object_or_404(Tag, TagID=tag_id)
    cards = tag.Cards.all().distinct()
    return render(request, 'cards_by_tag.html', {'tag_cards': cards})


def get_categories(request):
    """
    Возвращает все категории для представления в каталоге
    """
    # Проверка работы базового шаблона
    return render(request, 'base.html', info)


def get_detail_card_by_id(request, card_id):
    """
    /cards/<int:card_id>/detail/
    Возвращает шаблон cards/templates/cards/card_detail.html с детальной информацией по карточке
    """

    # Добываем карточку из БД через get_object_or_404
    # если карточки с таким id нет, то вернется 404
    card = {
        "card": get_object_or_404(Card, id=card_id),
        "menu": info["menu"],
    }

    return render(request, 'cards/card_detail.html', card, status=200)


