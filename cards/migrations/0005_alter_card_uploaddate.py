# Generated by Django 4.2 on 2024-03-18 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0004_alter_card_uploaddate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='UploadDate',
            field=models.DateTimeField(db_column='UploadDate'),
        ),
    ]
