from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from article.models import ArticlePost
from comment.forms import CommentForm
from .models import Comment
from notifications.signals import notify
from django.contrib.auth.models import User
from django.http import JsonResponse


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
                # 给其他用户发送通知
                """
                notify.send(actor, recipient, verb, target, action_object)
                actor：发送通知的对象
                recipient：接收通知的对象
                verb：动词短语
                target：链接到动作的对象（可选）
                action_object：执行通知的对象（可选）
                """
                if not parent_comment.user.is_superuser:
                    notify.send(
                        request.user,
                        recipient=parent_comment.user,
                        verb='回复了您',
                        target=article,
                        action_object=new_comment,
                    )
                # return HttpResponse('200 OK')
                return JsonResponse({"code": "200", "new_comment_id": new_comment.id})
            new_comment.save()
            # 给管理员发送通知
            if not request.user.is_superuser:
                notify.send(
                    request.user,
                    recipient=User.objects.filter(is_superuser=1),
                    verb='回复了您',
                    target=article,
                    action_object=new_comment,
                )
            redirect_url = article.get_absolute_url() + '#comment_elem_' + str(new_comment.id)
            return redirect(redirect_url)
        else:
            return HttpResponse('表单内容有误，请重新输入！！')
    elif request.method == 'GET':
        comment_form = CommentForm()
        return render(request, 'comment/reply.html', locals())
    else:
        return HttpResponse('发表评论仅接受POST请求。')
