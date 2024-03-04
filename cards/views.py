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
from .models import Card
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
    sort = request.GET.get('sort', 'date')
    sort_options = {
        'date': '-upload_date',
        'views': '-views',
        'adds': '-adds',
    }
    order = request.GET.get('order', 'desc')

    card_list = Card.objects.order_by(sort_options[sort])
    if order == 'asc':
        if sort == 'date':  # Добавляем условие для представления по умолчанию по дате
            card_list = card_list.order_by(sort_options[sort])
        else:
            card_list = card_list.reverse()
    else:
        if sort == 'date':  # Добавляем условие для представления по умолчанию по дате
            card_list = card_list.reverse()

    context = {
        'card_list': card_list,
        'current_sort': sort,
        'current_order': order
    }
    return render(request, 'catalog.html', context)


# def card_detail(request, card_id):
#     card = None
#     for c in cards_dataset:
#         if c['id_card'] == card_id:
#             card = c
#             break
#
#     if card is None:
#         return render(request, 'card_not_found.html')
#
#     return render(request, 'cards/card_detail.html', {'card': card})

def card_detail(request, card_id):
    card = get_object_or_404(Card, id=card_id)
    tags = json.loads(card.tags)
    context = {
        'card': card,
        'tags': tags
    }
    return render(request, 'cards/card_detail.html', context)


