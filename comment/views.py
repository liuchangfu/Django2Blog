from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from article.models import ArticlePost
from comment.forms import CommentForm
from .models import Comment


# Create your views here.

@login_required(login_url='/user_profile/login/')
def post_comment(request, article_id, parent_comment_id=None):
    article = get_object_or_404(ArticlePost, id=article_id)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            # 二级回复
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                # 若回复层级超过二级，则转换为二级
                new_comment.parent_id = parent_comment.get_root().id
                # 被回复人
                new_comment.reply_to = parent_comment.user
                new_comment.save()
                return HttpResponse('200 OK')
            new_comment.save()
            return redirect(article)
        else:
            return HttpResponse('表单内容有误，请重新输入！！')
    elif request.method == 'GET':
        comment_form = CommentForm()
        return render(request, 'comment/reply.html', locals())
    else:
        return HttpResponse('发表评论仅接受POST请求。')
