from django.shortcuts import render

from django.contrib.auth.backends import ModelBackend

# http://www.ywnds.com/?p=11973
from django.contrib import auth
User = auth.get_user_model()

from django.db.models import Q


# Create your views here.

# 认证后端
class CustomBackend(ModelBackend):
	'''
	自定义用户验证
	'''

	# 重写authenticate方法，默认不支持手机登录
	# authenticate 至少应该检查凭证, 如果凭证合法，它应该返回一个匹配于登录信息的 User 实例。如果不合法，则返回 None.
	def authenticate(self, username=None, password=None, **kwargs):
		try:
			# 用户名和手机都能登录
			user = User.objects.get(Q(username=username) | Q(mobile=username))
			if user.check_password(password):
				return user
		except Exception as e:
			return None