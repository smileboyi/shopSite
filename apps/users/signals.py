# https://blog.csdn.net/midion9/article/details/51372762
# https://segmentfault.com/a/1190000008455657
# https://docs.djangoproject.com/en/dev/ref/signals/
# signals机制不是异步执行，是同步执行，异步耗时任务应该用channels机制
from django.db.models.signals import post_save
from django.dispatch import receiver

# https://www.cnblogs.com/aguncn/p/6424158.html
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model
User = get_user_model()

"""
如果使用pre_save 或 post_save signal, 如果可以, 则将这些代码移到model的save()方法中.
同样如果使用pre_delete 或 post_delete signal, 如果可以, 则将这些代码移到model的delte()方法中.
"""


# 当django操作一个object或者请求的时候会自动发出一系列的signals，可以通过对这些signals注册listener，从而在相应的signals发出时执行一定的代码。
# 可以自定义signal,事件触发时，需要在视图里手动send signal。
@receiver(post_save,sender=User)
def create_user(sender,instance=None,created=False,**kwargs):   # model receiver定义默认写法

	# 是否新建，因为update的时候也会进行post_save
	if created:
		# instance就是User的实例
		password = instance.password
		instance.set_password(password)
		instance.save()