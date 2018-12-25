from django.urls import path, re_path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('page/<int:page>/', views.IndexView.as_view(), name='index_page'),
    path('article/<int:blog_id>/<slug:slug_name>',
         views.BlogDetailView.as_view(), name='blog_detail'),
    path('category/<int:category_id>/<slug>',
         views.BlogsWithCategoryView.as_view(), name="category"),
    # pre_path(r"^category/(?P<pk>\d+)/(?P<category_name>\w+)$",
    #        views.BlogsWithCategoryView.as_view(), name = "category"),

    path('categories', views.CategoriesView.as_view(), name="category_list"),
    path('archives', views.ArchiveView.as_view(), name="archives"),
    path('tag/<slug:tag_name>', views.BlogsWithTagView.as_view(), name='tag'),
    path('tags', views.TagsView.as_view(), name="tag_list"),
    path('about', views.AboutView.as_view(), name='about'),
]
