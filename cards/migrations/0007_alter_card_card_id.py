# Generated by Django 4.2 on 2024-03-18 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0006_alter_card_options_remove_cardtags_unique_card_tag_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='card_id',
            field=models.IntegerField(db_column='CardID', primary_key=True, serialize=False),
        ),
    ]
