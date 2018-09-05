from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from trade.serializer import ShopCartSerializer,ShopCartDetailSerializer,OrderDetailSerializer,OrderSerializer

from trade.models import ShoppingCart,OrderGoods,OrderInfo

from rest_framework import mixins
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




class OrderViewset(mixins.ListModelMixin,
										mixins.RetrieveModelMixin,
										mixins.CreateModelMixin,
										mixins.DestroyModelMixin,
										viewsets.GenericViewSet):
	'''
	订单管理
	list:
		获取个人订单
	delete:
		删除订单
	create：
		新增订单
	'''
	serializer_class = OrderSerializer
	authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
	permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

	def get_serializer_class(self):
		if self.action == 'retrieve':
			return OrderDetailSerializer
		return OrderSerializer

	def get_queryset(self):
		return OrderInfo.objects.filter(user=self.request.user)
	
	# 在订单提交保存之前还需要多两步步骤，所以重写perform_create，不只保存实例：
	# 1.将购物车中的商品保存到OrderGoods中；2.清空购物车
	def perform_create(self, serializer):
		order = serializer.save()

		# 中间的操作
		shop_carts = ShoppingCart.objects.filter(user=self.request.user)
		for shop_cart in shop_carts:
			# 订单商品数据来源于购物车商品数据
			order_goods = OrderGoods()
			order_goods.goods = shop_cart.goods
			order_goods.goods_num = shop_cart.nums
			order_goods.order = order
			order_goods.save()
			shop_cart.delete()

		return order