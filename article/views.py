from django.shortcuts import render
from django.http import HttpResponse
from article.models import ArticlePost
import markdown


# Create your views here.
def article_list(request):
    articles = ArticlePost.objects.all()
    return render(request, 'article/list.html', locals())


def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)
    # 将markdown语法渲染成html样式
    article.body = markdown.markdown(article.body,
                                     extensions=[
                                         # 包含 缩写、表格等常用扩展
                                         'markdown.extensions.extra',
                                         # 语法高亮扩展
                                         'markdown.extensions.codehilite',
                                         # 生成文章目录
                                         'markdown.extensions.toc',
                                     ])
    return render(request, 'article/detail.html', locals())
