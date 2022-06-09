from django import http
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
import re
# Create your views here.
from apps.users.models import User
import logging

# 记录异常
logger = logging.getLogger('django')

"""
断点优势：
    1.可以查看我们的方法是否被调用了
    2.可以查看程序运行过程中的数据
    3.查看程序的执行顺序是否和预期的一致
    
断点如何添加
    1.在函数（方法）的入口处
    2.不要再属性，类上加，没有用
    3.在需要验证的地方添加
"""

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

        # 2.6 验证用户协议是否勾选


        # 3.数据没有问题，入库，这里需要有模型
        # 当我们在操作外界资源时候（mysql，redis,file）的时候，我们最好进行try except异常处理
        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except Exception as e:
            logger.error(e)
            # return render(request, 'register.html', context={'error_message': '数据库异常'})
            return http.HttpResponseBadRequest('数据库异常')

        # 4.返回成功,跳转到首页

        # 注册完成之后，默认认为用户已经登录了
        # 保持状态
        # 登录的信息保存在session里面
        # 自己实现request.session

        # # 系统也能自己去帮助我们实现，登录状态保持
        from django.contrib.auth import login
        login(request, user)




        # return http.HttpResponse('注册成功')
        return redirect(reverse('contents:index'))  # 动态绑定
        # return redirect(reverse('/'))


"""
模板：
1.把需求写下来，
    前端需要收集什么，
    后端需要做什么
2.把大体思路写下来（后端）
3.把详细思路完善依稀
4.确定我们的请求方式和路由
"""


"""
1.把需求写下来，
    前端需要收集什么，
        当用户把用户名写完之后，前端应该收集用户名信息，传递给后端
        后端需要验证用户名是否重复
    后端需要做什么
2.把大体思路写下来（后端）
    前端：光标失去焦点后，发送一个ajax请求，这个请求包含用户名
    后端：接受数据，查询用户名
3.把详细思路完善依稀（后端）
    1.接收用户名
    2.查询数据库，通过查询记录的count来判断是否重复，0表示没有重复，1表示重复了
4.确定我们的请求方式和路由
    敏感数据，推荐使用post
    
    这里用GET   username/?username=XXX
    GET   username/xxxxx/count/
    /username/()/count
    
"""


class UsernameCountView(View):

    def get(self, request, username):
        # 1.接收用户名

        # 2.查询数据库，通过查询记录的count来判断是否重复，0表示没有重复，1表示重复了
        try:
            count = User.objects.filter(username=username).count()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': 400, 'errmsg': '数据库异常'})
        # 3 返回响应
        return http.JsonResponse({'code': 0, 'count': count})


"""
1.前端：把用户名和密码填写完成之后，发送给后端
后端： 验证用户名密码

2.大体思路
    a.后端接收数据
    b.验证数据
    c.如果验证成功则登录，验证不成功则登录失败

3.纯后端
    a.后端接收数据（username, password）
    b.判断参数是否齐全
    c.判断用户名是否符合规则
    d.判断密码是否符合规则
    e.用户名密码都没有问题，去验证用户名密码
    f如果成功则登录，状态保持
    g，登录不成功，则提示用户名或密码错误
    
4.请求方式和路由
     POST    login/
"""

class LoginView(View):

    def get(self, request):

        return render(request, 'login.html')

    def post(self, request):

        # 1.接收数据
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        remembered = data.get('remembered')
        # 验证数据是否缺失
        if not all([username, password]):
            return http.HttpResponseBadRequest('缺少必须参数')

        # 判断用户名是否符合规则
        if not re.match(r'[0-9a-zA-Z_]{5,20}',username):
            return http.HttpResponseBadRequest('用户名不合法')

        # 判断密码是否符合规则
        if not re.match(r'[0-9a-zA-Z_]{8,20}', password):
            return http.HttpResponseBadRequest('密码不合法')

        """
                # 5.验证用户名和密码
        # 验证有2种方式
        # ① 使用django的认证后端
        # ② 我们可以自己查询数据库( 根据用户名/手机号查询对应的user用户,再比对密码)

        from django.contrib.auth import authenticate
        # 默认的认证后端是调用了 from django.contrib.auth.backends import ModelBackend
        # ModelBackend 中的认证方法
        # def authenticate(self, request, username=None, password=None, **kwargs):

        # 如果用户名和密码正确,则返回user
        # 否则返回None
        """
        user = authenticate(uaername=username, password=password)

        if user is not None:
            # 登录
            login(request, user)

            # 状态保持
            if remembered == 'on':
                # request.session.set_expiry(seconds)
                request.session.set_expiry(30*24*2600)  # 30天
            else:
                request.session.set_expiry(0)  # 关闭就断开

            # 跳转到首页
            return redirect(reverse('contents:index'))
        else:
            # 验证不成功，提示账号密码错误
            return render(request, 'login.html', context={'account_errmsg': '用户名或密码错误'})

