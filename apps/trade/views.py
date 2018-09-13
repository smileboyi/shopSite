from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from trade.serializer import ShopCartSerializer,ShopCartDetailSerializer,OrderDetailSerializer,OrderSerializer

from trade.models import ShoppingCart,OrderGoods,OrderInfo

from rest_framework import mixins

from datetime import datetime
from utils.alipay import AliPay
from rest_framework.views import APIView
from shopSite.settings import ali_pub_key_path, private_key_path
from rest_framework.response import Response

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



# 文档：服务器异步通知页面特性
class AlipayView(APIView):
	def get(self, request):
		"""
		处理支付宝的return_url返回，完成交易后通知前端
		"""
		processed_dict = {}
		# 1. 获取GET中参数
		for key, value in request.GET.items():
			processed_dict[key] = value
		# 2. 取出sign
		sign = processed_dict.pop("sign", None)

		# 3. 生成ALipay对象
		alipay = AliPay(
			appid="2016091700531867",
			app_notify_url="http://47.104.158.4:8000/alipay/return/",
			app_private_key_path=private_key_path,
			alipay_public_key_path=ali_pub_key_path,
			debug=True,
			return_url="http://47.104.158.4:8000/alipay/return/"
		)

		verify_re = alipay.verify(processed_dict, sign)

		if verify_re is True:
			# 这里可以不做操作。因为不管发不发return url。notify url都会修改订单状态。
			# order_sn = processed_dict.get('out_trade_no', None)
			# trade_no = processed_dict.get('trade_no', None)
			# trade_status = processed_dict.get('trade_status', None)

			# existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
			# for existed_order in existed_orders:
			# 	existed_order.pay_status = trade_status
			# 	existed_order.trade_no = trade_no
			# 	existed_order.pay_time = datetime.now()
			# 	existed_order.save()

			response = redirect("/index/#/app/home/member/order")
			return response
		else:
			response = redirect("index")
			return response

	def post(self, request):
		"""
		处理支付宝的notify_url，完成交易后通知后端（通知支付宝success）
		"""
		# 存放post里面所有的数据
		processed_dict = {}
		# 取出post里面的数据
		for key, value in request.POST.items():
				processed_dict[key] = value
		# 把signpop掉，文档有说明
		sign = processed_dict.pop("sign", None)

		# 生成一个Alipay对象
		alipay = AliPay(
			appid="2016091700531867",
			app_notify_url="http://47.104.158.4:8000/alipay/return/",
			app_private_key_path=private_key_path,
			alipay_public_key_path=ali_pub_key_path,
			debug=True,
			return_url="http://47.104.158.4:8000/alipay/return/"
		)

		# 进行验证
		verify_re = alipay.verify(processed_dict, sign)

		# 验签成功success，失败不success
		if verify_re is True:
			# 商户网站唯一订单号
			order_sn = processed_dict.get('out_trade_no', None)
			# 支付宝系统交易流水号
			trade_no = processed_dict.get('trade_no', None)
			# 交易状态
			trade_status = processed_dict.get('trade_status', None)

			# 查询数据库中订单记录
			existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
			for existed_order in existed_orders:
				# 订单商品项
				order_goods = existed_order.goods.all()

				# 商品销量增加订单中数值
				for order_good in order_goods:
					goods = order_good.goods
					goods.sold_num += order_good.goods_num
					goods.save()

				# 更新订单状态
				existed_order.pay_status = trade_status
				existed_order.trade_no = trade_no
				existed_order.pay_time = datetime.now()
				existed_order.save()

			return Response("success")