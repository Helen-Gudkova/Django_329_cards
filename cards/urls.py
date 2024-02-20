# /cards/urls.py
from django.urls import path
from . import views

# Префикс /cards/
urlpatterns = [
    path('', views.catalog, name='catalog'),  # Общий каталог всех карточек
    path('<int:card_id>/detail/', views.card_detail, name='card_detail'),
    #path('categories/<slug:slug>/', views.get_cards_by_category, name='category'),  # Карточки по категории
    #path('tags/<slug:slug>/', views.get_cards_by_tag, name='tag'),  # Карточки по тегу
    #path('<int:card_id>/detail/', views.get_detail_card_by_id, name='detail_card_by_id'),
    # Детальная информация по карточке
]
