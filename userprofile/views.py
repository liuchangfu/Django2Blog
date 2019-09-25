from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from userprofile.forms import UserProfileForm, UserRegisterForm, ProFileFrom
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from userprofile.models import ProFile


# Create your views here.
# 用户登录
def user_login(request):
    # 从 get 或者 post 请求中获取 next 参数值
    # get 请求中，next 通过 url 传递，即 /?next=value
    # post 请求中，next 通过表单传递，即 <input type="hidden" name="next" value="{{ next }}"/>
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    print(redirect_to)
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
                # 登录成功之后，跳转到登录前的页面
                return redirect(request.GET.get('next', '/'))
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
    # 退出登录后，跳转到退出前的页面
    return redirect(request.GET.get('next', '/'))


# 用户注册
def user_register(request):
    if request.method == 'POST':
        print(request.POST.get('password'))
        print(request.POST.get('password2'))
        print(request.POST.get('username'))
        user_register_form = UserRegisterForm(request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            # 保存好数据后立即登录并返回博客列表页面
            login(request, new_user)
            return redirect('article:article_list')
        else:
            return HttpResponse('注册表单输入有误，请重新输入！！！')
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        return render(request, 'userprofile/register.html', locals())
    else:
        return HttpResponse('请使用GET或POST提交数据！！')


# 验证用户是否登录的装饰器
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


@login_required(login_url='/user_profile/login/')
def edit(request, id):
    user = User.objects.get(id=id)
    # user_id 是 OneToOneField 自动生成的字段
    # profile = ProFile.objects.get(user_id=id)
    if ProFile.objects.filter(user_id=id).exists():
        profile = ProFile.objects.get(user_id=id)
    else:
        profile = ProFile.objects.create(user_id=id)
    if request.method == 'POST':
        # 验证修改数据者，是否为用户本人
        if request.user != user:
            return HttpResponse('您无权修改此用户信息!!')
        # 上传的文件保存在 request.FILES 中，通过参数传递给表单类
        profile_from = ProFileFrom(request.POST, request.FILES)
        if profile_from.is_valid():
            profile.phone = profile_from.cleaned_data['phone']
            profile.bio = profile_from.cleaned_data['bio']
            if 'avatar' in request.FILES:
                profile.avatar = profile_from.cleaned_data['avatar']
            profile.save()
            # 带参数的 redirect()
            return redirect('user_profile:edit', id=id)
        else:
            return HttpResponse('注册表单输入有误。请重新输入~')
    elif request.method == 'GET':
        profile_from = ProFileFrom()
        return render(request, 'userprofile/edit.html', locals())
    else:
        return HttpResponse("请使用GET或POST请求数据")
