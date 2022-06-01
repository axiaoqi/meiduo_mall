from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment


# 过滤器
def environment(**option):

    # 1.创建Environment实例
    env = Environment(**option)

    # 2.指定或更新jinja2的函数，指向django的指定过滤器
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })

    # 返回环境的实例
    return env
