import re
from datetime import datetime,timedelta

from shopSite.settings import REGEX_MOBILE

from users.models import VerifyCode

# https://blog.csdn.net/u013210620/article/details/79869661
from rest_framework import serializers

from django.contrib.auth import get_user_model
User = get_user_model()



# 注意是Serializer不是ModelSerializer
class SmsSerializer(serializers.Serializer):
	'''
	手机号码
	'''
	mobile = serializers.CharField(max_length=11)

	# 自定义验证逻辑: https://blog.csdn.net/l_vip/article/details/79156113
	def validate_mobile(self,mobile):
		# 是否已经注册
		if User.objects.filter(mobile=mobile).count():
			raise serializers.ValidationError("用户已经存在")
		
		# 是否合法
		if not re.match(REGEX_MOBILE,mobile):
			raise serializers.ValidationError("手机号码非法")

		# 一分钟前的时间点,timedelta为时间差
		one_mintes_ago = datetime.now() - timedelta(hours=0,minutes=1,seconds=0)
		# 控制验证码发送频率，前端也可以控制请求频率，但可以通过手段跳过，所以后端要有完整的检验过程
		if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
			raise serializers.ValidationError("距离上一次发送未超过60s")

		return mobile

