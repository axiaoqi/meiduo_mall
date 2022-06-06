from django import http
from django.shortcuts import render

# Create your views here.
from django.views import View
from apps.verifications.constants import IMAGE_CODE_EXPIRE_TIME

"""
模板：
1.把需求写下来，
    前端需要收集什么，
        生成一个uuid随机码，把这个随机码给后端,减少服务器压力
    后端需要做什么
        生成图片验证码，把这个图片验证码的内容保存到raedis内，redis的数据是uuid:验证码
2.把大体思路写下来（后端）
    1.生成图片验证码和图片内容
    2.1.连接redis
    2.2将图片验证码保存起来uuid:验证码，有有效期
    3.返回图片验证码
3.把详细思路完善依稀
4.确定我们的请求方式和路由
    GET方式
        /imagecode/(?P<uuid>[\w-]+)/
"""
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection


class ImageCodeView(View):

    def get(self, request, uuid):
        # uuid= request.GET.get('uuid')
        """
        1.生成图片验证码和图片内容
        2.1.连接redis
        2.2将图片验证码保存起来uuid:验证码，有有效期
        3.返回图片验证码
        """
        text, image = captcha.generate_captcha()
        # 使用django-redis
        redis_conn = get_redis_connection('code')
        # 使用settings里面的code，redis的2号库， 120是秒。时间
        # redis_conn.setex('img_%s'%uuid, 120, text)  # 这里可以给uuid添加一个前缀，可加可不加
        redis_conn.setex('img_%s'%uuid, IMAGE_CODE_EXPIRE_TIME, text)  # 把时间定义为常量，增加了代码的可读性

        # 返回图片验证码
        # content_type 是MIME类型，告知浏览器这是个图片
        return http.HttpResponse(image, content_type='image/jpeg')











