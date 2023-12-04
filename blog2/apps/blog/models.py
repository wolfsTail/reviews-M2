from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey

from apps.services.utils import unique_slugify


class Post(models.Model):
    """
    Модель, отражающая структуру публикации блога
    """

    STATUS_OPTIONS = (
        ('published', 'Опубликовано'),
        ('draft', 'Черновик')
    )

    title = models.CharField(verbose_name='Название записи', max_length=128)
    slug = models.SlugField(verbose_name='URL', max_length=128, blank=True)
    description = models.TextField(verbose_name='Описание', max_length=512)
    text = models.TextField(verbose_name='Текст записи')
    category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name='Категория')
    thumbnail = models.ImageField(
        verbose_name='Изображение записи',
        blank=True,
        upload_to='images/thumbnails/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))]
    )
    status = models.CharField(choices=STATUS_OPTIONS, default='published', verbose_name='Статус записи', max_length=10)
    create = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')
    update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    author = models.ForeignKey(to=User, verbose_name='Автор', on_delete=models.SET_DEFAULT, related_name='author_posts',
                               default=1)
    updater = models.ForeignKey(to=User, verbose_name='Обновил', on_delete=models.SET_NULL, null=True,
                                related_name='updater_posts', blank=True)
    fixed = models.BooleanField(verbose_name='Прикреплено', default=False)

    class Meta:
        db_table = 'blog_post'
        ordering = ['-fixed', '-create']
        indexes = [models.Index(fields=['-fixed', '-create', 'status'])]
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Category(MPTTModel):
    """
    Модель, отражающая структуру категории
    """
    title = models.CharField(max_length=64, verbose_name='Заголовок категории')
    slug = models.SlugField(max_length=64, verbose_name='URL категории', blank=True)
    description = models.TextField(verbose_name='Описание категории', max_length=256)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        related_name='children',
        verbose_name='Родительская категория'
    )

    class MPTTMeta:
        """
        Сортировка вложенности
        """
        order_insertion_by = ('title',)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'app_categories'
    
    def get_absolute_url(self):
        return reverse('post_by_category', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title