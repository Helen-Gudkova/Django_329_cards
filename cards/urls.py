# /cards/urls.py
from django.urls import path
from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import CatalogView
from django.views.decorators.cache import cache_page
# Префикс /cards/
urlpatterns = [
    # Общий каталог всех карточек
    path('catalog/', login_required(CatalogView.as_view()), name='catalog'),
    path('categories/', views.get_categories, name='categories'),  # Список всех категорий
    path('categories/<slug:slug>/', views.get_cards_by_category, name='category'),  # Карточки по категории
    path('tags/<int:tag_id>/', views.get_cards_by_tag, name='get_cards_by_tag'),  # Карточки по тегу
    path('<int:pk>/detail/', views.CardDetailView.as_view(), name='detail_card_by_id'),
    path('add/', views.AddCardCreateView.as_view(), name='add_card'),  # Добавление карточки
    path('<int:pk>/edit/', views.CardUpdateView.as_view(), name='edit_card'),  # Редактирование карточки
    path('preview_card_ajax/', views.preview_card_ajax, name='preview_card_ajax'),
]

