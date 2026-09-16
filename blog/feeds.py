from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post

class LatestPostsFeed(Feed):
    title = "Tech Blogs - Latest Posts"
    link = reverse_lazy('blog:home')
    description = "New published posts on the blog."

    def items(self):
        return Post.objects.filter(status='published').order_by('-created_at')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.content, 30)

    def item_pubdate(self, item):
        return item.created_at
