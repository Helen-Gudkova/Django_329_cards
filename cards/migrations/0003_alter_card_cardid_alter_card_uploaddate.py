# Generated by Django 4.2 on 2024-03-18 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_category_tag_users_rename_adds_card_favorites_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='CardID',
            field=models.BigIntegerField(db_column='CardID', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='card',
            name='UploadDate',
            field=models.DateTimeField(db_column='UploadDate'),
        ),
    ]
