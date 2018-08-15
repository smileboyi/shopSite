import re
from datetime import datetime,timedelta

from shopSite.settings import REGEX_MOBILE

from users.models import VerifyCode

# https://blog.csdn.net/u013210620/article/details/79869661
from rest_framework import serializers

from rest_framework.validators import UniqueValidator

from django.contrib.auth import get_user_model
User = get_user_model()



# 注意是Serializer不是ModelSerializer,通过serializer自定义字段
class SmsSerializer(serializers.Serializer):
	'''
	手机号码
	'''
	# 使用自定义字段，值由前端页面通过表单直接提供，不在数据库里面得到
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



# 在视图中对从前端返回的字段验证变为在序列字段中验证，视图不再处理数据，由序列化完成
# 视图集专门设置分页，搜索，过滤，排序等可插拔的功能
class UserRegSerializer(serializers.ModelSerializer):
	'''
	用户注册
	'''
	# 注册数据由用户提供，并添加验证机制
	code = serializers.CharField(required=True,write_only=True,max_length=4,min_length=4,
															error_messages={
																"blamk": "请输入验证码",
																"required": "请输入验证码",
																"max_length": "验证码格式错误",
																"min_length": "验证码格式错误",
															},
															help_text="验证码")

	username = serializers.CharField(label='用户名',required=True,allow_blank=False,help_text='用户名',
																	validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])

	def validate_code(self,code):
		# 用户注册，已post方式提交注册信息，post的数据都保存在initial_data里面
		# username就是用户注册的手机号，验证码按添加时间倒序排序，为了后面验证过期，错误等
		verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
		if verify_records:
			# 取最近的验证码，其他无效(可以删除数据库中的垃圾数据，防止冗余)
			last_record = verify_records[0]
			# 5分钟前的时间点
			five_mintes_ago = datetime.now()-timedelta(hours=0,minutes=5,seconds=0)

			if five_mintes_ago > last_record.add_time:
				raise serializers.ValidationError("验证码过期")

			if last_record.code != code:
				raise serializers.ValidationError("验证码错误")
		else:
			raise serializers.ValidationError("验证码错误")

	def validate(self,attrs):
		# attrs是字段验证合法之后返回的总的dict
		attrs['mobile'] = attrs['username']
		del attrs['code']
		# 返回的attrs将保存到数据库中（用户提供的数据=>验证=>合法=>保存）
		return attrs

	class Meta:
		model = User
		fields = ('username','code','mobile')