from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from django.utils import timezone

from .models import Post, Category, Project


class PortfolioStaticSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return ['portfolio:home_page', 'portfolio:post_list', 'portfolio:project_list', ]

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        return timezone.now()


class PostSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return Post.active_objs.all()

    def lastmod(self, item):
        return item.datetime_updated


class PostSearchSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return ['python', 'django', 'web+development']

    def location(self, item):
        # Generate the URLs for each item
        return reverse('portfolio:post_search') + '?q=' + item


class CategorySitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return Category.objects.all()

    def lastmod(self, item):
        return item.datetime_updated


class ProjectSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Project.active_objs.all()

    def lastmod(self, item):
        return item.datetime_updated
