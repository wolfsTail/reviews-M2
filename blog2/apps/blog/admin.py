from django.contrib import admin

from django_mptt_admin.admin import DjangoMpttAdmin
from .models import Category, Post, Comment, Rating


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdminPage(DjangoMpttAdmin):
    pass


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """
    Админ-панель модели рейтинга
    """
    pass