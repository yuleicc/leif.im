"""leif_im URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from apps.blog import views
from sitemaps import BlogSitemap
from django.contrib import admin
from apps.blog.views import IndexView
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'blog': BlogSitemap,
}

handler404 = 'apps.blog.views.handle_page_not_found'
handler500 = 'apps.blog.views.server_error_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.blog.urls', 'blog')),
    path('robots.txt', TemplateView.as_view(
        template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('api/v1/', include('apis.api_v1.blog.urls', 'api-v1'))
]
