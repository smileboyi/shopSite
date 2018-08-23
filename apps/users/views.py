
from django.contrib.auth.backends import ModelBackend

# http://www.ywnds.com/?p=11973
from django.contrib import auth
User = auth.get_user_model()

from users.models import VerifyCode
from django.db.models import Q

from rest_framework import mixins,viewsets
from rest_framework.mixins import CreateModelMixin

from users.serializers import SmsSerializer,UserRegSerializer

from utils.yunpian import YunPian
from shopSite.settings import APIKEY

from rest_framework.response import Response
from rest_framework import status

# jwt介绍：https://blog.csdn.net/liuwenbiao1203/article/details/52351772
from rest_framework_jwt.serializers import jwt_encode_handler,jwt_payload_handler

# 传入一个列表，元组或字符串，返回随机项
from random import choice

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



# 仅仅是发送验证码的视图，不会暂存code，配合用户注册时需要通过VerifyCode保存一份code
class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
	'''
	发送短信验证码
	'''
	serializer_class = SmsSerializer

	# 云片不提供验证码的生成，只负责发送
	def generate_code(self):
		'''
		生成四位数字的验证码
		'''
		seeds = "1234567890"
		random_str = []
		for i in range(4):
			random_str.append(choice(seeds))
		return "".join(random_str)
	
	# 继承CreateModelMixin,重写create
	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		# 验证数据的合法性，如果不合法则不会执行后面的代码，并且返回带有mobile属性的dict给前端
		serializer.is_valid(raise_exception=True)

		code = self.generate_code()   # 4位数
		mobile = serializer.validated_data["mobile"]  # 手机号码
		yun_pian = YunPian(APIKEY)  # YunPian实例

		sms_status = yun_pian.send_sms(code=code, mobile=mobile)
		# 发送状态识别
		if sms_status["code"] != 0:
			# 失败=>请求错误
			return Response({
				"mobile": sms_status["msg"]
			}, status=status.HTTP_400_BAD_REQUEST)
		else:
			# 成功=>成功创建
			code_record = VerifyCode(code=code, mobile=mobile)
			code_record.save()
			return Response({ "mobile": mobile }, status=status.HTTP_201_CREATED)



class userViewset(CreateModelMixin,
									mixins.RetrieveModelMixin,
									mixins.UpdateModelMixin,
									viewsets.GenericViewSet):
	'''
	用户
	'''
	serializer_class = UserRegSerializer
	queryset = User.objects.all()

	authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

	def create(self, request, *args, **kwargs):
		# 前面不变，保存数据
		serializer = self.get_serializer(data=request.data)
		# raise_exception=True,一旦验证不通过，不再往下执行，直接引发异常
		serializer.is_valid(raise_exception=True)
		user = self.perform_create(serializer)

		# 定义给返回给前端的响应体信息,默认只有username和mobile字段
		re_dict = serializer.data
		# 使用jwt_payload_handler将user构造成payload，header已经指定好了
		payload = jwt_payload_handler(user)
		# 对payload进行加密
		re_dict["token"] = jwt_encode_handler(payload)
		re_dict["name"] = user.name if user.name else user.username
		# 响应头部数据
		headers = self.get_success_headers(serializer.data)

		# 创建一个用户时，还需要返回给前端具体的创建情况，返回name和token就行了，然后用户再用密码登录网站
		return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

	# 根据请求场景设置动态权限，不是所有场景权限是相同的
	def get_permissions(self):
		# 当是get请求获取用户信息时，需要登录
		if self.action == "retrieve":
			return [permissions.IsAuthenticated()]
		elif self.action == "create":
			return []

		return []

	# 根据请求场景动态使用那个序列化方式
	def get_serializer_class(self):
		if self.action == "retrieve":
			# 获取个人信息时
			return UserDetailSerializer
		elif self.action == "create":
			# 注册的时候
			return UserRegSerializer
		# 修改个人信息时
		return UserDetailSerializer

	# 虽然继承了Retrieve可以获取用户详情，但是并不知道用户的id，所有要重写get_object方法
	# 重写get_object方法，就知道是哪个用户了
	def get_object(self):
			return self.request.user

	# 保存实例(必须要重写此方法，不然创建不了实例)
	def perform_create(self, serializer):
		return serializer.save()

	'''
	不需要重写
	def get_success_headers(self, data):
		try:
			return {'Location': data[api_settings.URL_FIELD_NAME]}
		except (TypeError, KeyError):
			return {}
	'''





"""
				post													response
					|														↗		 ↑
|----------------------------------------------------|
|					↓													/			 |					|
|		获取相关serializer							/			  |					 |
|					↓					N							/				 |					|
|			进行数据验证------------>Exception		 |					|
|					| Y															 |					|
|				保存实例													  |					 |
|					↓																 |					|
|				Response---------------------------|					|
|																		CreateModelMixin	|
|-----------------------------------------------------|

"""