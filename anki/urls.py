"""
anki/urls.py
"""
from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from django.conf import settings
from django.urls import path, include
from cards import views

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),
    # Маршруты для меню
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    # Маршруты подключенные из приложения cards
    path('cards/', include('cards.urls')),
    path('users/', include('users.urls')),  # Подключение URL-путей из приложения users

]

if settings.DEBUG:
    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                      # другие URL-паттерны
                  ] + urlpatterns
