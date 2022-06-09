from django import http
from django.shortcuts import render

# Create your views here.
from django.views import View
from apps.verifications.constants import IMAGE_CODE_EXPIRE_TIME, SMS_CODE_EXPIRE_TIME
from libs.ronglian_sms_sdk.SendMessage import send_message

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
from utils.response_code import RETCODE

# 添加记录
import logging
logger = logging.getLogger('django')


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


"""
用户点击获取短信验证码按钮，我们能够给用户发送短信

1. 把需求写下来
    前端：手机号，用户输入的图片验证码内容和uuid
    通过ajax发送给后端
2.后端
    接收参数
    验证参数
    发送短信
3.详细研究一下后端
    1.接收参数（手机号，图片验证码，uuid）
    2.验证参数
        验证手机号
        这三个参数必须有
    3.验证用户输入的图片验证码和服务器保存的图片验证码一致
        3。1用户的图片验证码
        3.2服务器的验证码
        3.3比对
    4，生成一个随机短信吗
    5.把短信验证码保存起来
        redis， key:value, 60s有效
    6.最后发送
        借助第三方库发送
4，确定我们的请求方式和路由
    GET
        /smscode/mobile/uuid/imagecode/
        
        /smscode/?mobile=xxxx&uuid=xxxx&imagecode=xxxx
        
        /smscode/mobile/?uuid=xxx&imagecode=xxxx
        
        /sms_codes/(?P<mobile>1[3-9]\d{9})/
    POST

"""


class SmsCodeView(View):

    def get(self, request, mobile):

        # 接受参数
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')

        # 判断三个参数都有
        if not all([mobile, image_code, uuid]):
            # 响应码
            return http.JsonResponse({'code': RETCODE.NECESSARYPARAMERR, 'errormsg': '参数不齐'})

        try:
            # 获取服务器验证码
            redis_conn = get_redis_connection('code')
            redis_code = redis_conn.get('img_%s' % uuid)

            # 判断验证码过期
            if redis_code is None:
                return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '验证码过期'})

            # 添加一个删除图片验证码的逻辑
            # 1. 删除可以防止用户再次比对
            # 2. 从redis数据保存在内存中，不用的话就删除，节省内存空间
            redis_conn.delete('img_%s' % uuid)
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': 'redis有异常'})


        # 获取reidis的数据都是bytes类型，大小写不同
        if redis_code.decode().lower() != image_code.lower():
            return http.JsonResponse({'code': RETCODE.SMSCODERR, 'errmsg': '短信验证码错误'})


        # 防止乱发短信
        # 这里需要判断标记是否是1
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            return http.JsonResponse({'code': RETCODE.SMSCODERR, 'errmsg': '操作太频繁'})


        # 生成一个随机短信码
        from random import randint
        sms_code = '%06d' % randint(0, 999999)  # '%06d' % 用0补齐 ，也可直接10000， 999999

        # 性能优化
        # # ①创建管道
        # pipe = redis_conn.pipeline()
        # # ② 执行
        # pipe.setex('sms_%s' % mobile, SMS_CODE_EXPIRE_TIME, sms_code)
        # pipe.setex('send_flag_%s' % mobile, 60, 1)
        # # ③ 让管道执行
        # pipe.execute()


        # 把短信验证码保存起来，redis， redis mobile: value
        redis_conn.setex('sms_%s'%mobile, SMS_CODE_EXPIRE_TIME, sms_code)


        # redis里面添加标记，避免重复发送,60s有效
        redis_conn.setex('send_flag_%s' % mobile, 60, 1)


        # 发送短息
        # send_message('1', mobile, (sms_code, SMS_CODE_EXPIRE_TIME/60))
        # 我们的函数需要通过delay调用，才能添加到broker（队列中）
        from celery_tasks.sms.tasks import send_sms_code
        # send_sms_code的参数平移到delay中
        send_sms_code.delay(mobile, sms_code)


        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok'})









