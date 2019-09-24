from django.db import models
from django.contrib.auth.models import User
from article.models import ArticlePost


# Create your models here.

class Comment(models.Model):
    article = models.ForeignKey(ArticlePost, on_delete=models.CASCADE, related_name='comments', verbose_name='评论文章')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='评论用户')
    body = models.TextField(verbose_name='评论内容')
    created = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.body[:20]