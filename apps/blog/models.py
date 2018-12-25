from django.db import models

# Create your models here.
import re
import uuid
import datetime
from uuslug import slugify
from django.urls import reverse
from django.utils.timezone import now
from django.contrib.auth.models import User
# from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType


class BaseModel(models.Model):
    slug = models.SlugField(default='no-slug', max_length=160, blank=True)
    created_at = models.DateTimeField('创建时间', default=now)
    updated_at = models.DateTimeField('更新时间', default=now)

    class Meta:
        abstract = True


class Category(models.Model):
    """
    分类
    """
    NOT_SHOW = 0
    SHOW = 1
    IS_SHOW = (
        (NOT_SHOW, 'NR - 不显示'),
        (SHOW, 'R - 显示'),
    )

    uuid = models.UUIDField('uuid', default=uuid.uuid4, editable=False)
    title = models.CharField('名称', max_length=50, db_index=True, unique=True)
    slug = models.SlugField(default='no-slug', max_length=160, blank=True)
    icon = models.CharField('图标', max_length=50, null=True, blank=True)
    type = models.CharField('类型', max_length=64, null=True, blank=True)
    is_show = models.BooleanField('是否显示', choices=IS_SHOW, default=NOT_SHOW)
    created_at = models.DateTimeField('创建时间', default=now)
    updated_at = models.DateTimeField('更新时间', default=now)

    class Meta:
        ordering = ['title', ]
        verbose_name = '文章分类'
        verbose_name_plural = '文章分类'

    def __str__(self):
        return self.title


class BlogQuerySet(models.QuerySet):
    def published(self):
        """
        已发布的文章
        """
        return self.filter(status='p')

    def public(self):
        """
        公开的文章
        :return:
        """
        return self.filter(is_public=True)


class BlogManager(models.Manager):
    def get_queryset(self):
        return BlogQuerySet(self.model, using=self._db).order_by('-publish_time')

    def published(self):
        return self.get_queryset().published()

    def public(self):
        return self.get_queryset().public()


class Blog(models.Model):
    STATUS_CHOICES = (
        ('d', "草稿"),
        ('p', "已发布"),
    )
    uuid = models.UUIDField('uuid', default=uuid.uuid4, editable=False)
    title = models.CharField('标题', max_length=150, db_index=True, unique=True)
    slug = models.SlugField(default='no-slug', max_length=160, blank=True)
    cover = models.URLField('封面', default='', blank=True)
    snippet = models.CharField('摘要', max_length=500, default='')
    content = models.TextField('内容', )
    publish_time = models.DateTimeField('发表时间', null=True)
    status = models.CharField(
        '状态', max_length=1, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    is_public = models.BooleanField('公开', default=True)
    is_top = models.BooleanField('置顶', default=False)
    access_count = models.IntegerField('浏览量', default=1, editable=False)
    category = models.ForeignKey(
        'Category', verbose_name='分类', on_delete=models.CASCADE, blank=False, null=False)
    tags = models.ManyToManyField('Tag', verbose_name='标签集合', blank=True)
    tags.help_text = '标签'
    author = models.ForeignKey(
        User, verbose_name='作者',  on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField('创建时间', default=now, editable=False)
    updated_at = models.DateTimeField('更新时间', default=now, editable=False)
    objects = BlogManager()

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'

    def save(self, *args, **kwargs):
        self.snippet = self.snippet or self.content[:140]
        modified = kwargs.pop("modified", True)
        if modified:
            self.updated_at = datetime.datetime.utcnow()
        if not self.slug or self.slug == 'no-slug' or not self.id:
            # Only set the slug when the object is created.
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:blog_detail', args=(self.id, self.slug))

    def __str__(self):
        return self.title

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model),
                       args=(self.id,))


class Tag(models.Model):
    """
    小标签
    """
    title = models.CharField('名称', max_length=50, db_index=True, unique=True)
    created_at = models.DateTimeField('创建时间', default=now)
    updated_at = models.DateTimeField('更新时间', default=now)

    def save(self, *args, **kwargs):
        self.title = re.sub("\s", "", self.title)
        super(Tag, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'

    def __str__(self):
        return self.title
