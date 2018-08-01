from django.shortcuts import render

from django.contrib.auth.backends import ModelBackend

from django.contrib.auth import get_user_model

from django.db.models import Q


User = get_user_model()
# Create your views here.

# 认证后端
class CustomBackend(ModelBackend):
	'''
	自定义用户验证
	'''

	# 当调用authenticate()时 —— 如何登入一个用户中所描述的 —— Django会尝试所有的认证后台进行认证。
	# 如果后台引发PermissionDenied 异常，认证将立即失败。Django 不会检查后面的认证后台。
	# authenticate 至少应该检查凭证, 如果凭证合法，它应该返回一个匹配于登录信息的 User 实例。如果不合法，则返回 None.
	def authenticate(self, username=None, password=None, **kwargs):
		try:
			# 用户名和手机都能登录
			user = User.objects.get(Q(username=username) | Q(mobile=username))
			if user.check_password(password):
				return user
		except Exception as e:
			return None