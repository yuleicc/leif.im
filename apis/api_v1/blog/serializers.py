from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets
from apps.blog.models import Blog, Category, Tag


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "title", "slug")


class TagsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "title")


class BlogSerializer(serializers.ModelSerializer):
    category = CategorySerializers()
    tags = TagsSerializers(many=True)

    class Meta:
        model = Blog
        fields = ('id', 'title', 'slug', 'cover', 'snippet',
                  'content', 'publish_time', 'status', 'is_public',
                  'is_top', 'access_count', 'category', 'tags')
