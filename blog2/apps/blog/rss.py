from django.contrib.syndication.views import Feed
from django.db.models.base import Model
from django.urls import reverse
from .models import Post


class LatestPostFeed(Feed):
    title = 'Личнео мнение - акутуальное'
    description = 'Свежие статьи на портале'
    link =  '/feeds/'    

    def items(self):
        return Post.objects.order_by('-update')[:3]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return item.description
    
    def item_link(self, item):
        return reverse('post_detail', args=(item.slug,))