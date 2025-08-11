from django.urls import path
from downloader import views
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import Sitemap
from django.urls import path
from django.shortcuts import reverse

class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ['index', 'download_video', 'blog'] 
    
    def location(self, item):
        return reverse(item)

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('', views.index, name='index'),
    path('download/', views.download_video, name='download_video'),
    path('blog/', views.blog, name='blog'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),

]

