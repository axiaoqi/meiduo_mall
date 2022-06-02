"""meiduo_mall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from django.http import HttpResponse
def log(request):
    """
    1.日志的作用是为了方便我们的项目部署上线之后分析问题
    2.日志的配置，我们直接复制到settings里面就行了
    3.级别：debug，info,warning,error,critical
    4.使用
        import logging
        logger = logging.getLogger(setting_name)

        logger.info()
        logger.warning()
        logger.error

    :param request:
    :return:

    """
    # 1.导入
    import logging
    # 2.创建日志器
    logger = logging.getLogger('django')
    # 3.记录
    logger.info('info--')
    logger.warning('warning---')

    return HttpResponse('log')


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^log/$', log)
    url(r'^', include('apps.users.urls', namespace='users'))
]

