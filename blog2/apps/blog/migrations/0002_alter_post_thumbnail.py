# Generated by Django 5.0 on 2023-12-04 16:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to='images/thumbnails/%Y/%m/%d/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))], verbose_name='Изображение записи'),
        ),
    ]
