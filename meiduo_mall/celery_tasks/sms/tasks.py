# 这个文件名必须是tasks
# 3.设置生产者(任务--可能就是一个函数)tasks
#     任务的本质就是函数
#     这个函数必须要被celery的实例对象的task装饰器装饰
#     必须调用celery实例对象的自动检测来检测任务
from apps.verifications.constants import SMS_CODE_EXPIRE_TIME
from libs.ronglian_sms_sdk.SendMessage import send_message
from celery_tasks.main import app


@app.task
def send_sms_code(mobile, sms_code):

    send_message('1', mobile, (sms_code, SMS_CODE_EXPIRE_TIME / 60))
