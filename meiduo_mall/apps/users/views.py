import re

from django.http import HttpResponse, JsonResponse
from django.urls import reverse

from apps.users.models import User
from django import http
from django.shortcuts import render, redirect
from django.views import View


class RegisterView(View):
    """
    用户注册
    """
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        # 接收参数
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        mobile = request.POST.get("mobile")

        # 验证数据
        if not all([username, password, password2, mobile]):
            return http.HttpResponseBadRequest("参数补全")

        # 判断用户名是否符合逻辑
        if not re.match(r'[a-zA_Z0-9_-]{5, 20}', username):
            return http.HttpResponseBadRequest("用户名 不符合规则")

        # 判断密码是否符合逻辑
        if not re.match(r'[a-zA-Z0-9]{8,20}', password):
            return http.HttpResponseBadRequest("密码不符合规则")

        # 校验密码一致性
        if password != password2:
            return http.HttpResponseBadRequest("密码不一致")

        # 校验手机号
        if not re.match(r'1[345678]\d{9}', mobile):
            return http.HttpResponseBadRequest("手机号不符合规则")

        # 数据入库
        # 密码是明文  可以进行加密处理
        user = User.objects.create_user(username=username, password=password, mobile=mobile)

        # 设置session信息
        # 借助于系统的session设置
        from django.contrib.auth import login
        login(request, user)

        # 返回相应  跳转到首页去
        # return redirect(reverse("contents:index"))
        return HttpResponse("注册成功")

class UsernameCountView(View):

    def get(self, request, username):
        count = User.objects.filter(username=username).count()

        # 返回相应
        return JsonResponse({"count": count})
        pass




