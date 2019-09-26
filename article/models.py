from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from mdeditor.fields import MDTextField
from django.urls import reverse


# Create your models here.

class ArticleColumn(models.Model):
    # 栏目标题
    title = models.CharField(max_length=100, verbose_name='标题')
    # 创建时间
    created = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']
        verbose_name_plural = '文章分类'
        verbose_name = '文章分类'


class ArticlePost(models.Model):
    # 文章作者。参数on_delete用于指定数据删除方式
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    # 文章标题
    title = models.CharField(max_length=100, verbose_name='标题')
    # 文章正文
    # body = models.TextField(verbose_name='正文')
    # 文章正文 以markdown形式
    body = MDTextField(verbose_name='正文')
    # 文章创建时间，参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    create = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    # 文章更新时间
    update = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    # 浏览数
    total_views = models.PositiveIntegerField(default=0, verbose_name='文章浏览数')
    # 文章栏目的 “一对多” 外键
    column = models.ForeignKey(ArticleColumn, null=True, blank=True, on_delete=models.CASCADE, related_name='article',
                               verbose_name='文章分类')

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        return self.title

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        ordering = ['-create']
        verbose_name_plural = '文章'
        verbose_name = '文章'

    # 获取文章地址
    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])
