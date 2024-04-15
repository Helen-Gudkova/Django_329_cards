from datetime import timezone, datetime
from django.utils import timezone
from django.db import models
from django.urls import reverse
import logging
from django.contrib.auth import get_user_model
import datetime
import uuid

# Создаем или получаем экземпляр логгера
logger = logging.getLogger(__name__)

# Устанавливаем базовый уровень логирования. В продакшене вы можете выбрать уровень WARNING или ERROR
logging.basicConfig(level=logging.DEBUG)
# Create your models here.
class Category(models.Model):
    Category_id = models.AutoField(primary_key=True, db_column='CategoryID')
    Name = models.TextField(unique=True, null=False, db_column='Name')

    class Meta:
        db_table = 'Categories'

    def __str__(self):
        return self.Name
class Tag(models.Model):
    TagID = models.AutoField(primary_key=True, db_column='TagID')
    Name = models.TextField(unique=True, null=False, db_column='Name')

    class Meta:
        db_table = 'Tags'

    def __str__(self):
        return self.Name


class CardTags(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    card = models.ForeignKey('Card', on_delete=models.CASCADE, db_column='CardID')
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE, db_column='TagID')

    class Meta:
        db_table = 'CardTags'
        managed = False
        unique_together = (('card', 'tag'),)

    def __str__(self):
        return f'{self.card} - {self.tag}'

class Users(models.Model):
    user_id = models.AutoField(primary_key=True, db_column='UserID')
    username = models.TextField(null=False, db_column='UserName')

    class Meta:
        db_table = 'Users'


class Card(models.Model):
    class Status(models.IntegerChoices):
        UNCHECKED = 0, 'Не проверено'
        CHECKED = 1, 'Проверено'

    card_id = models.IntegerField(primary_key=True, db_column='CardID')  # Старое поле CardID
    Question = models.TextField(null=False, db_column='Question')
    Answer = models.TextField(null=False, db_column='Answer')
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='CategoryID')
    UploadDate = models.DateTimeField(auto_now_add=True, db_column='UploadDate')
    Views = models.IntegerField(default=0, db_column='Views')
    Favorites = models.IntegerField(default=0, db_column='Favorites')
    check_status = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.UNCHECKED, db_column='CheckStatus')
    tags = models.ManyToManyField(Tag, through=CardTags, related_name='Cards')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, db_column='AuthorID', verbose_name='Автор', related_name='cards', null=True, default=None)

    class Meta:
        db_table = 'Cards'

    def __str__(self):
        return self.Question
# Опишем get_absolute_url для модели Card - метод, который возвращает URL карточки
    # Псевдоним - detail_card_by_id
    # reverse - возвращает URL по псевдониму
    def get_absolute_url(self):
        return reverse('detail_card_by_id', kwargs={'pk': self.card_id})

    def save(self, *args, **kwargs):
        # Логируем перед сохранением объекта
        logger.debug(f'Сохранение карточки {self.card_id}, значения: {self.__dict__}')

        super().save(*args, **kwargs)  # Вызываем оригинальный метод save




