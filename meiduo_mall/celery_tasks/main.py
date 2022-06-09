"""
Celery 将这三个串联起来
生产者   队列     消费者
tasks   broker  workers

1.创建Celery
2.设置队列broker
3.设置生产者(任务--可能就是一个函数)tasks
    任务的本质就是函数
    这个函数必须要被celery的实例对象的task装饰器装饰
    必须调用celery实例对象的自动检测来检测任务
4.设置消费者workers
    celery -A proj worker -l info
    celery -A celery实例对象的文件 worker -l info

    celery -A celery_tasks.main worker -l info


测试windows10好像报错
https://blog.csdn.net/m0_64224975/article/details/125071918
解决办法
pip install eventlet
然后最后添加一个参数就好了
celery -A celery_tasks.main worker -l info -P eventlet

celery -A celery_tasks.main worker -l info -P eventlet


官方文档：https://docs.celeryq.dev/en/master/getting-started/index.html

https://docs.celeryq.dev/en/master/django/first-steps-with-django.html#using-celery-with-django
"""

# 1.Set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings")

# 2.创建celery实例对象
from celery import Celery
# Celery的第一个参数是main， 习惯上填写当前脚本的工程名就可以
# 这个就是给celery的实例起个名字，这个名字唯一就可以
app = Celery('celery_tasks')

# 3.celery设置broker（队列），可以选redis，也可以是RabbitMQ
# config_from_object的参数就是我们配置文件的路径
app.config_from_object('celery_tasks.config')


# 4.让celery自动检测任务
# autodiscover_tasks 的参数是列表
# 列表的元素是：任务的包路径
app.autodiscover_tasks(['celery_tasks.sms'])  # 这样就可以自动检测任务了


# 5.设置消费者
# celery -A celery_tasks.main worker -l info -P eventlet




