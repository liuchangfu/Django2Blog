from django.contrib import admin
from article.models import ArticlePost


# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'create', 'update']
    list_display_links = ['title']


admin.site.register(ArticlePost, ArticleAdmin)

# admin后台，登录标题
admin.site.site_header = '博客管理后台'
# admin后台的网页标题
admin.site.site_title = '博客后台'
