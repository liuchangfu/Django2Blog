from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import ProFile


# Register your models here.

# 定义一个行内 admin
class ProFileInline(admin.StackedInline):
    model = ProFile
    can_delete = False
    verbose_name_plural = '用户信息'


# 将 Profile 关联到 User 中
class UserAdmin(BaseUserAdmin):
    inlines = (ProFileInline,)


# 重新注册 User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
