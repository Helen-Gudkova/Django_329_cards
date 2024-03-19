"""
python manage.py createsuperuser - создание суперпользователя
"""

from django.contrib import admin
from .models import Card, Tag, Category, CardTags

admin.site.register(Card)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(CardTags)
