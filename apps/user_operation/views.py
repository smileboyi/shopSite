from rest_framework import viewsets,mixins

from user_operation.models import UserFav,UserLeavingMessage,UserAddress

from user_operation.serializers import UserFavSerializer,UserFavDetailSerializer,LeavingMessageSerializer,AddressSerializer

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly

# Create your views here.


class UserFavViewset(viewsets.GenericViewSet, 
											mixins.ListModelMixin,     # 获取列表
											mixins.CreateModelMixin,   # 添加收藏
											mixins.DestroyModelMixin): # 取消收藏
	'''
	用户收藏
	'''
	serializer_class = UserFavSerializer

	authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
	# IsAuthenticated：必须登录用户；IsOwnerOrReadOnly：必须是当前登录的用户
	permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)

	# 搜索的字段
	lookup_field = 'goods_id'

	def get_serializer_class(self):
		if self.action == "list":
			# 当需要返回更多信息时，而不是外键id,可以定义一个嵌套序列类
			return UserFavDetailSerializer
		elif self.action == "create":
			# 收藏时只要id就行了
			return UserFavSerializer
		# 取消收藏等操作
		return UserFavSerializer

	# 覆盖queryset = UserFav.objects.all()
	def get_queryset(self):
		# 只能查看当前登录用户的收藏，不会获取所有用户的收藏
		return UserFav.objects.filter(user=self.request.user)


"""
只有登录用户才可以收藏
用户只能获取自己的收藏，不能获取所有用户的收藏
JSONWebTokenAuthentication认证不应该全局配置，因为用户获取商品信息或者其它页面的时候并不需要此认证，所以这个认证只要局部中添加就可以
删除settings中的'rest_framework_jwt.authentication.JSONWebTokenAuthentication'
"""





class LeavingMessageViewset(mixins.ListModelMixin,
														mixins.DestroyModelMixin,
														mixins.CreateModelMixin,
														viewsets.GenericViewSet):
	'''
	list:
		获取用户留言
	create:
		添加留言
	delete:
		删除留言功能
	'''
	serializer_class = LeavingMessageSerializer

	authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
	permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

	# 删除成功后没有返回信息，可以通过响应头部判断，或者改写destroy方法
	# 只能看到自己的留言
	def get_queryset(self):
		return UserLeavingMessage.objects.filter(user=self.request.user)




class AddressViewset(viewsets.ModelViewSet):
	'''
	收货地址管理
	list:
		获取收货地址
	create:
		添加收货地址
	update:
		更新收货地址
	delete:
		删除收货地址
	'''
	serializer_class = AddressSerializer

	authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
	permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

	def get_queryset(self):
		return UserAddress.objects.filter(user=self.request.user)