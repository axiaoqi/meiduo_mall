from django import http
from django.shortcuts import render
from django.views import View
import re
# Create your views here.
from apps.users.models import User


class RegisterView(View):
    """
    1.用户名是否重复，是一个需求（开发一个视图）
        用户名长度6-20个字符
    2.密码有长度限制，6-20个字符，字母，数字，_，不要有空格
    3.确认密码跟密码一致
    4.手机号,手机号满足规则，11位，是否符合规则，手机号是否重复
    5.图片验证码是一个后端功能，图片验证码是为短信服务的，为了防止黑客胡乱调用短信验证码
        captcha，避免浪费验证码，图形验证码最牛的网站，12306

    6.短信发送
    7.必须同意协议
    8.注册按钮也是一个功能

    必须和后端交互的是：
        用户名、手机号是否重复
        图片验证码
        短信
        注册功能
    """
    def get(self, request):

        return render(request, 'register.html')

    def post(self, request):
        """
        1.接受前段提交的用户名，密码，手机号
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        password2 = data.get('password2')
        mobile = data.get('mobile')
        2.数据的验证，作为后端开发者，不相信前端提交的任何数据
            2.1 验证必传的数据是否有值

            2.2 判断用户名是否符合规则
            2.3 判断密码 是否符合规则
            2.4 判断确认密码是否和密码一致
            2.5判断手机号是否符合规则
        3.数据没有问题，入库，这里需要有模型
        4.返回值
        """

        # 1.接受前段提交的用户名，密码，手机号
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        password2 = data.get('password2')
        mobile = data.get('mobile')
        # 2.1 验证必传的数据是否有值
        # all([el, el, el]) el必徐有值，只要有一个为None，则为False
        if not all([username, password, password2, mobile]):
            return http.HttpResponseBadRequest('参数有问题')
        # 2.2 判断用户名是否符合规则，正则表达式
        if not re.match(r'[0-9a-zA-Z_]{5,20}', username):
            return http.HttpResponseBadRequest('用户名不合法')
            # 2.3 判断密码 是否符合规则
        if not re.match(r'[0-9a-zA-Z_]{5,20}', password):
            return http.HttpResponseBadRequest('密码不合法')

        # 2.4 判断确认密码是否和密码一致
        if password2 != password:
            return http.HttpResponseBadRequest('密码不一致')

        # 2.5判断手机号是否符合规则
        if not re.match(r'1[3-9]\d{9}', mobile):
            return http.HttpResponseBadRequest('手机号不符合规则')

        # 3.数据没有问题，入库，这里需要有模型
        user = User.objects.create_user(username=username, password=password, mobile=mobile)

        # 返回成功
        return http.HttpResponse('注册成功')




