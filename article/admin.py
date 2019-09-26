from django.contrib import admin
from article.models import ArticlePost, ArticleColumn


# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'create', 'update']
    list_display_links = ['title']


class ArticleColumnAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created']
    list_display_links = ['title']


admin.site.register(ArticlePost, ArticleAdmin)
admin.site.register(ArticleColumn, ArticleColumnAdmin)

# admin后台，登录标题
admin.site.site_header = '博客管理后台'
# admin后台的网页标题
admin.site.site_title = '博客后台'
