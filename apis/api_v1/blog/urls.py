from django.urls import path
from .import views

app_name = 'api-v1'

urlpatterns = [
    path('blog', views.BlogListView.as_view(), name='blog_list'),
    path('blog/<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),
]
