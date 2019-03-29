from django.contrib.sitemaps import Sitemap
from apps.blog.models import Blog
from django.urls import reverse


class BlogSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5
    protocol = "https"

    def items(self):
        return Blog.objects.filter(is_public=True).filter(status='p').order_by('-created_at')

    def lastmod(self, item):
        return item.updated_at
