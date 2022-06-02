from django.db import models

# Create your models here.
"""
1.自己定义模型
class User(models.Model)
    username
    password
    mobile
 自己定义模型的话密码是明文，我们要自己完成验证等一些问题
    
 2.学习基础时候，django有自带的用户管理   ，admin后台管理，也有用户信息的保存和认证，密码是密文，也可以验证用户信息

所以我们想给用户 用django自带的用户模型
    
"""
# 来自于这里
from django.contrib.auth.models import AbstractUser


"""
当系统的类或方法不能满足我们的需求，我们就继承重写
"""


# 我们添加一个手机号，继承重新
class User(AbstractUser):

    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')

    class Meta:
        """
        修改表名字
        """
        db_table = 'tb_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

"""
上门的模型，需要替换一下系统
settings.py
# 通过提供一个值给AUTH_USER_MODEL设置，指向自定义的模型，django允许你覆盖默认的user模型
# AUTH_USER_MODEL = '子应用名.模型类'
AUTH_USER_MODEL = 'users.User'

运行命令
python manage.py makemigrations
"""