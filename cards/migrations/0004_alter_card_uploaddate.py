# Generated by Django 4.2 on 2024-03-18 18:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_alter_card_cardid_alter_card_uploaddate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='UploadDate',
            field=models.DateTimeField(db_column='UploadDate', default=django.utils.timezone.now),
        ),
    ]
