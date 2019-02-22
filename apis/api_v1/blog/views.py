from rest_framework import generics
from apps.blog.models import Blog
from apis.api_v1.blog.serializers import BlogSerializer, CategorySerializers


# class BlogListViewSet(viewsets.ModelViewSet):
class BlogListView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializers = CategorySerializers(queryset, many=True)
    serializer_class = BlogSerializer


class BlogDetailView(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
