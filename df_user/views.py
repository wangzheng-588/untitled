# -*- coding: utf-8 -*-
import hashlib

import simplejson
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from df_user.BaseReq import toResult
from df_user.models import UserInfo


def register(request):
    context = {"username": "", "password": "", "cpassword": "", "email": ""}
    return render(request, 'df_user/register.html', context)


def register_handler(request):
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    ucpwd = post.get('cpwd')
    uemail = post.get('email')

    if uname.strip() == '':
        return redirect('user:register')

    if upwd != ucpwd:
        return redirect('user:register')

    if uemail.strip() == '':
        return redirect('user:register')

    # 判断用户是否注册过
    if len(UserInfo.objects.filter(uname=uname)) == 0:
        # 创建对象
        user = UserInfo()
        user.uname = uname

        # 密码加密
        md5 = hashlib.md5()
        md5.update(upwd.encode("utf8"))
        upwd1 = md5.hexdigest()

        user.upwd = upwd1
        user.uemail = uemail
        user.save()

        # 注册成功转到登录页面
        return redirect('user:login')
    else:
        return redirect('user:register')


def register_user_exist(request):
    count = len(UserInfo.objects.filter(uname=request.GET.get('user_name')))
    if count > 0:
        result = toResult(msg="用户名已存在", content={"count": count})
    else:
        result = toResult(msg="成功", content={"count": count})
    return JsonResponse(result)


def login(request):
    return render(request, 'df_user/login.html')


def login_handler(request):
    username = request.POST.get("username", "")
    password = request.POST.get("pwd", "")

    if username is None or username.strip() == "" or password is None or password.strip() == "":
        result = toResult(code=205, msg="用户名与密码不能为空")
        return HttpResponse(simplejson.dumps(result))

    user_count = len(UserInfo.objects.filter(uname=username))

    if user_count == 1:

        # 密码加密
        md5 = hashlib.md5()
        md5.update(password.encode("utf8"))
        md5pwd = md5.hexdigest()

        userResult = UserInfo.objects.filter(uname=username, upwd=md5pwd)
        if len(userResult) == 1:

            print("密码正确")
            print(md5pwd)
            print(password)

            userInfo = UserInfo()
            userInfo.uname = userResult[0].uname
            userInfo.uemail = userResult[0].uemail
            retult = toResult(msg="登录成功")
            return HttpResponse(simplejson.dumps(retult))
        else:
            result = toResult(code=201, msg="密码错误")
            print("密码错误")
            print(md5pwd)
            print(password)
            return HttpResponse(simplejson.dumps(result))

    else:
        retult = toResult(code=202, msg="用户名错误")
        return HttpResponse(simplejson.dumps(retult))


def user_center_order(request):
    return render(request, "df_user/user_center_info.html")
