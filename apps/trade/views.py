from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from trade.serializer import ShopCartSerializer,ShopCartDetailSerializer

from trade.models import ShoppingCart
# Create your views here.


class ShoppingCartViewset(viewsets.ModelViewSet):
	'''
	购物车功能
	list:
		获取购物车详情
	create：
		加入购物车
	delete：
		删除购物记录
	'''
	serializer_class = ShopCartSerializer

	authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
	permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

	def get_serializer_class(self):
		if self.action == 'list':
			# 给列表补充详情数据
			return ShopCartDetailSerializer
		else:
			return ShopCartSerializer

	def get_queryset(self):
		return ShoppingCart.objects.filter(user = self.request.user)
