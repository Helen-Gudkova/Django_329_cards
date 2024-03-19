# /cards/urls.py
from django.urls import path
from . import views

# Префикс /cards/
urlpatterns = [
    path('', views.catalog, name='catalog'),  # Общий каталог всех карточек
    path('catalog/', views.catalog, name='catalog'),
    #path('<int:card_id>/detail/', views.card_detail, name='card_detail'),
    #path('cards/<int:card_id>/detail/', views.card_detail, name='card_detail'),
    path('tags/<int:tag_id>/', views.get_cards_by_tag, name='cards_by_tag'),
    path('categories/', views.get_categories, name='categories'),  # Список всех категорий
    path('tags/<int:tag_id>/', views.get_cards_by_tag, name='get_cards_by_tag'), #Карточки по тег
    path('<int:card_id>/detail/', views.get_detail_card_by_id, name='detail_card_by_id'),
    path('cards/<int:card_id>/', views.card_detail, name='card_detail'),
      # Детальная информация по карточке
]
