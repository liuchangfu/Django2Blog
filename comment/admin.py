from django.contrib import admin
from comment.models import Comment


# Register your models here.


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'article', 'user', 'body', 'created']
    list_display_links = ['article']


admin.site.register(Comment, CommentAdmin)
