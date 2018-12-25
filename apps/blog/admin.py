from django.contrib import admin
import datetime
# Register your models here.
from .forms import BlogForm
from .models import Tag, Blog, Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'icon', 'type', 'is_show')


class TagAdmin(admin.ModelAdmin):
    pass


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_public',
                    'status', 'publish', 'access_count')
    fields = (
        'title',
        'cover',
        'content',
        'snippet',
        ('is_public', 'is_top',),
        ('category', 'tags')
    )

    exclude = ('publish_time',)
    search_fields = ('title',)
    ordering = ('-publish_time',)
    list_per_page = 60
    form = BlogForm
    actions = ['make_published']

    def create_time(self, obj):
        return obj.publish_time.strftime('%Y-%m-%d')

    create_time.short_description = "创建时间"

    def publish(self, obj):
        if obj.publish_time:
            return obj.publish_time.strftime('%Y-%m-%d')
        else:
            return ''

    publish.short_description = "发布时间"

    def make_published(self, request, queryset):
        rows_updated = 0
        for entry in queryset:
            entry.status = 'p'
            rows_updated += 1
            if entry.publish_time is None:
                entry.publish_time = datetime.datetime.now()
            entry.save()
        message_bit = "%s 篇博客 " % rows_updated
        self.message_user(request, "%s 成功发布" % message_bit)

    make_published.short_description = "发表"

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        if '_save' in request.POST.keys():
            # 只有是操作状态的文章才更新发布时间
            if obj.status == 'd':
                obj.publish_time = datetime.datetime.now()
            obj.status = Blog.STATUS_CHOICES[1][0]
        elif '_save_as_draft' in request.POST.keys():
            obj.status = Blog.STATUS_CHOICES[0][0]
        super(BlogAdmin, self).save_model(request, obj, form, change)
        # obj.save()

    def change_view(self, request, object_id, form_url='', extra_context=None):
        more_context = {}
        more_context.update(extra_context or {})
        return super(BlogAdmin, self).change_view(request, object_id, form_url, more_context)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Tag, TagAdmin)
