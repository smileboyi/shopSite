from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser

"""
自定义用户模型：https://www.cnblogs.com/robinunix/p/7922403.html
"""


# 用户信息
class UserProfile(AbstractUser):
	GENDER_CHOICES = (("male", u"男"),("female", u"女"))
	name = models.CharField("姓名",max_length=30,null=True,blank=True)
	birthday = models.DateField("出生年月",null = True,blank = True)
	gender = models.CharField("性别",max_length=6, choices=GENDER_CHOICES, default="female")
	mobile = models.CharField("电话",max_length=11,null=True, blank=True)
	email = models.EmailField("邮箱",max_length=100, null=True, blank=True)

	class Meta:
		verbose_name = "用户信息"
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.username



# 验证码
class VerifyCode(models.Model):
	# 一般还有个类型字段，登录注册找回密码等等
	code = models.CharField("验证码",max_length=10)
	mobile = models.CharField("电话",max_length=11)
	# 需要一个时间记录，以控制获取验证码频率，前端虽然能控制频率，但可以通过手段跳过检查
	add_time = models.DateTimeField("添加时间",default=datetime.now)

	class Meta:
		verbose_name = "短信验证"
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.code