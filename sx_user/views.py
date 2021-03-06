from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from sx_user.models import UserModel, UserTicketModel
from utils.functions import get_ticket


def register(request):
    # 注册
    if request.method == 'GET':
        return render(request, 'user/register.html')

    if request.method == 'POST':
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        password_c = request.POST.get('cpwd')
        email = request.POST.get('email')
        # 验证参数都不能为空
        if not all([username, password, password_c, email]):
            data = {
                'msg': '信息请填写完整'
            }
            return render(request, 'user/register.html', data)
        # 加密password
        password = make_password(password)
        password_c = make_password(password_c)
        # 创建用户并添加到数据库
        UserModel.objects.create(username=username,
                                 password=password,
                                 password_c=password_c,
                                 email=email)
        # 注册成功跳转到登陆页面
        return HttpResponseRedirect(reverse('user:login'))


def login(request):
    # 登陆
    if request.method == 'GET':
        return render(request, 'user/login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        data = {}
        # 验证信息是否填写完整
        if not all([username, password]):
            data['msg'] = '用户名或者密码不能为空'
        # 验证用户是否注册
        if UserModel.objects.filter(username=username).exists():
            user = UserModel.objects.get(username=username)
            # 验证密码是否正确
            if check_password(password, user.password):
                # 如果密码正确将ticket值保存在cookie中
                ticket = get_ticket()
                response = HttpResponseRedirect(reverse('store:index'))
                out_time = datetime.now() + timedelta(days=1)
                response.set_cookie('ticket', ticket, expires=out_time)
                # 保存ticket值到数据库user_ticket表中
                UserTicketModel.objects.create(user=user,
                                               out_time=out_time,
                                               ticket=ticket)

                return response
            else:
                msg = '用户名或密码错误'
                return render(request, 'user/login.html', {'msg': msg})
        else:
            msg = '用户名不存在,请注册后在登陆'
            return render(request, 'user/login.html', {'msg': msg})


def user_center_info(request):
    if request.method == 'GET':
        return render(request, 'user/user_center_info.html')


def user_center_order(request):
    if request.method == 'GET':
        return render(request, 'user/user_center_order.html')


def user_center_site(request):
    if request.method == 'GET':
        return render(request, 'user/user_center_site.html')