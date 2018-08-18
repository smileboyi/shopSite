
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



class userViewset(CreateModelMixin,viewsets.GenericViewSet):
	'''
	用户
	'''
	serializer_class = UserRegSerializer
	queryset = User.objects.all()


