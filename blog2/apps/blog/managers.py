from django.db import models


class PostManager(models.Manager):
    """
    Менеджер для фильтрафии по критерию - Опубликовано
    """

    def all(self):
        return self.get_queryset().select_related("author", "category").filter(status="published")