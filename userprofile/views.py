from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from userprofile.forms import UserProfileForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.
# 用户登录
def user_login(request):
    if request.method == 'POST':
        user_login_form = UserProfileForm(request.POST)
        if user_login_form.is_valid():
            # cleaned_data 清洗出合法数据
            # 检验账号、密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个 user 对象
            user = authenticate(username=user_login_form.cleaned_data['username'],
                                password=user_login_form.cleaned_data['password'])
            if user:
                # 将用户数据保存在 session 中，即实现了登录动作
                login(request, user)
                return redirect('article:article_list')
            else:
                return HttpResponse('账号或密码输入有误，请重新输入！！')
        else:
            return HttpResponse('账号或密码输入不合法！')
    elif request.method == 'GET':
        user_login_form = UserProfileForm()
        return render(request, 'userprofile/login.html', locals())
    else:
        return HttpResponse('请使用GET或POST请求数据！！')


# 用户退出
def user_logout(request):
    logout(request)
    return redirect('article:article_list')


# 用户注册
def user_register(request):
    if request.method == 'POST':
        print(request.POST.get('password'))
        print(request.POST.get('password2'))
        user_register_form = UserRegisterForm(request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect('article:article_list')
        else:
            return HttpResponse('注册表单输入有误，请重新输入！！！')
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        return render(request, 'userprofile/register.html', locals())
    else:
        return HttpResponse('请使用GET或POST提交数据！！')


@login_required(login_url='/user_profile/login/')
def user_delete(request, id):
    user = User.objects.get(id=id)
    # 验证登录用户、待删除用户是否相同
    if request.user == user:
        logout(request)
        # 退出登录，删除数据并返回博客列表
        user.delete()
        return redirect('article:article_list')
    else:
        HttpResponse('您没有删除权限！！！')
