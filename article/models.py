from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from mdeditor.fields import MDTextField
from django.urls import reverse
from taggit.managers import TaggableManager
from PIL import Image
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit


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
    # 文章标签
    tags = TaggableManager(blank=True, verbose_name='文章标签')
    # 文章标题图
    # avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True, verbose_name='文章缩略图')
    avatar = ProcessedImageField(
        # 上传位置
        upload_to='article/%Y%m%d',
        # 处理规则,图片宽度为400
        processors=[ResizeToFit(width=400)],
        # 存储格式
        format='JPEG',
        # 图片质量
        options={'quality': 100},
        verbose_name='文章缩略图'
    )

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

    def save(self, *args, **kwargs):
        # 调用原有的 save() 的功能
        article = super(ArticlePost, self).save(*args, **kwargs)

        # 固定宽度缩放图片大小
        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x, y) = image.size
            new_x = 400
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)
        return article
