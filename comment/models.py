from django.db import models
from django.contrib.auth.models import User
from article.models import ArticlePost
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.

class Comment(MPTTModel):
    article = models.ForeignKey(ArticlePost, on_delete=models.CASCADE, related_name='comments', verbose_name='评论文章')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='评论用户')
    # body = models.TextField(verbose_name='评论内容')
    body = RichTextField(verbose_name='评论内容')
    created = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                            verbose_name='父评论')
    reply_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='replyers',
                                 verbose_name='回复')

    # class Meta:
    #     ordering = ['-created']
    #     verbose_name_plural = '评论管理'
    #     verbose_name = '评论管理'

    class MPTTMeta:
        order_insertion_by = ['created']

    class Meta:
        verbose_name_plural = '评论管理'
        verbose_name = '评论管理'

    def __str__(self):
        return self.body[:20]
