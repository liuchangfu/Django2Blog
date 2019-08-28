from django.shortcuts import render, redirect
from django.http import HttpResponse
from article.models import ArticlePost
import markdown
from article.forms import ArticlePostForm
from django.contrib.auth.models import User


# Create your views here.
def article_list(request):
    # 取出所有博客文章
    articles = ArticlePost.objects.all()
    return render(request, 'article/list.html', locals())


def article_detail(request, id):
    # 获取某篇文章的详细信息
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


# 创建文章
def create(request):
    # 判断用户是否提交数据
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        article_post_create = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_create.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_create.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            new_article.author = User.objects.get(id=1)
            # 将新文章保存到数据库中
            new_article.save()
            # 完成后返回到文章列表
            return redirect('article:article_list')
        else:
            # 如果数据不合法，返回错误信息
            return HttpResponse('表单内容有误，请重新填写！！')
    else:
        # 创建表单类实例
        article_post_create = ArticlePostForm()
        return render(request, 'article/create.html', locals())


# 删除文章
def delete(request, id):
    # 根据 id 获取需要删除的文章
    article = ArticlePost.objects.get(id=id)
    # 调用.delete()方法删除文章
    article.delete()
    # 完成删除后返回文章列表
    return redirect('article:article_list')


def article_update(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新titile、body字段
    GET方法进入初始表单页面
    id： 文章的 id
    """
    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)
    # 判断用户是否为 POST 提交表单数据
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            article.title = article_post_form.cleaned_data['title']
            article.body = article_post_form.cleaned_data['body']
            # article.title = request.POST['title']
            # article.body = request.POST['body']
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect('article:article_detail', id=id)
        else:
            # 如果数据不合法，返回错误信息
            return HttpResponse('表单填写错误，请重新填写！！')
    else:
        # 如果用户 GET 请求获取数据
        article_post_from = ArticlePostForm()
        return render(request, 'article/update.html', locals())
