from django.shortcuts import render
from django.views import View
# Create your views here.


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
        2.入库，这里需要有模型
        3.返回值
        """
        pass