from django.shortcuts import render, redirect
from django.http import HttpResponse
from article.models import ArticlePost, ArticleColumn
from comment.models import Comment
import markdown
from article.forms import ArticlePostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from comment.forms import CommentForm


# Create your views here.
def article_list(request):
    search = request.GET.get('search')
    print('search:', search)
    order = request.GET.get('order')
    print('order:', order)
    column = request.GET.get('column')
    print('column:', column)
    tag = request.GET.get('tag')
    print('tag:', tag)
    # 初始化查询集
    article_list = ArticlePost.objects.all()
    # 搜索查询集
    if search:
        article_list = article_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search = ''

    # 栏目查询集
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)

    # 标签查询集
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])

    # 查询集排序
    if order == 'total_views':
        article_list = article_list.order_by('-total_views')
    # 用 Q对象 进行联合搜索,搜词可通过标题或文章正文搜索
    # if search:
    #     # 最热面包屑搜索
    #     if order == 'total_views':
    #         article_list = ArticlePost.objects.filter(Q(title__icontains=search) | Q(body__icontains=search)).order_by(
    #             '-total_views')
    #     else:
    #         # 最新面包屑搜索
    #         article_list = ArticlePost.objects.filter(Q(title__icontains=search) | Q(body__icontains=search))
    # else:
    #     # 将 search 参数重置为空
    #     search = ''
    #     # 最热面包屑搜索
    #     if order == 'total_views':
    #         article_list = ArticlePost.objects.all().order_by('-total_views')
    #         order = 'total_views'
    #     else:
    #         # 最新面包屑搜索
    #         article_list = ArticlePost.objects.all()

    # 每页显示10篇文章
    paginator = Paginator(article_list, 10)
    # 获取 url 中的页码
    page = request.GET.get('page')
    try:
        # 将导航对象相应的页码内容返回给 articles
        articles = paginator.page(page)
    except PageNotAnInteger:
        # 如果请求的页数不是整数，返回第一页。
        articles = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        articles = paginator.page(paginator.num_pages)
    return render(request, 'article/list.html', locals())


def article_detail(request, id):
    # 获取某篇文章的详细信息
    article = ArticlePost.objects.get(id=id)
    # 统计浏览量
    article.total_views += 1
    article.save(update_fields=['total_views'])
    comments = Comment.objects.filter(article=id)
    # 将markdown语法渲染成html样式
    md = markdown.Markdown(article.body,
                           extensions=[
                               # 包含 缩写、表格等常用扩展
                               'markdown.extensions.extra',
                               # 语法高亮扩展
                               'markdown.extensions.codehilite',
                               # 生成文章目录
                               'markdown.extensions.toc',
                           ])
    article.body = md.convert(article.body)
    toc = md.toc
    # 引入评论表单
    comment_form = CommentForm()
    return render(request, 'article/detail.html', locals())


# 创建文章
@login_required(login_url='/user_profile/login/')
def article_create(request):
    # 判断用户是否提交数据
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        article_post_from = ArticlePostForm(request.POST, request.FILES)
        # 判断提交的数据是否满足模型的要求
        if article_post_from.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_from.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            new_article.author = User.objects.get(id=request.user.id)
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            # 将新文章保存到数据库中
            new_article.save()
            # 新增代码，保存 tags 的多对多关系
            article_post_from.save_m2m()
            # 完成后返回到文章列表
            return redirect('article:article_list')
        else:
            # 如果数据不合法，返回错误信息
            return HttpResponse('表单内容有误，请重新填写！！')
    else:
        # 创建表单类实例
        columns = ArticleColumn.objects.all()
        article_post_from = ArticlePostForm()
        return render(request, 'article/create.html', locals())


# 删除文章
def article_delete(request, id):
    print(request.user)
    # 根据 id 获取需要删除的文章
    article = ArticlePost.objects.get(id=id)
    # 过滤非作者的用户
    if article.author != request.user:
        return HttpResponse("抱歉，你无权删除这篇文章。")
    # 调用.delete()方法删除文章
    article.delete()
    # 完成删除后返回文章列表
    return redirect('article:article_list')


# 更新文章
def article_update(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新titile、body字段
    GET方法进入初始表单页面
    id： 文章的 id
    """
    print(request.user)
    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)
    # 过滤非作者的用户
    if article.author != request.user:
        return HttpResponse("抱歉，你无权修改这篇文章。")
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
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None
            if request.FILES.get('avatar'):
                article.avatar = request.FILES.get('avatar')
            article.tags.set(*request.POST.get('tags').split(','), clear=True)
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect('article:article_detail', id=id)
        else:
            # 如果数据不合法，返回错误信息
            return HttpResponse('表单填写错误，请重新填写！！')
    else:
        # 如果用户 GET 请求获取数据
        article_post_from = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        tags = ','.join([x for x in article.tags.names()])
        return render(request, 'article/update.html', locals())
