from trade.models import ShoppingCart,OrderGoods,OrderInfo
from goods.models import Goods

from goods.serializers import GoodsSerializer

from rest_framework import serializers

from utils.alipay import AliPay
from MxShop.settings import ali_pub_key_path, private_key_path



class ShopCartSerializer(serializers.Serializer):
	'''
	购物车
	'''
	user = serializers.HiddenField(
		default = serializers.CurrentUserDefault()
	)
	nums = serializers.IntegerField(required=True,label='数量',min_value=1,
																	error_messages={
																		'min_value': '商品数量不能小于一',
																		'required': '请选择购买数量'
																	})
	# 这里是继承Serializer，必须指定queryset对象，如果继承ModelSerializer则不需要指定
	goods = serializers.PrimaryKeyRelatedField(required=True,queryset=Goods.objects.all())

	def create(self,validated_data):
		# view中:self.request.user；serizlizer中:self.context["request"].user
		user = self.context['request'].user
		nums = validated_data['nums']
		goods = validated_data['goods']

		existed = ShoppingCart.objects.filter(user=user,goods=goods)

		if existed:
			existed = existed[0]
			# 更新数量
			existed.nums += nums
			existed.save()
		else:
			existed = ShoppingCart.objects.create(**validated_data)

		return existed

	# Seriazer中并没有重新update方法，所以添加一个update方法
	def update(self, instance, validated_data):
		# 只更新商品数量
		instance.nums = validated_data["nums"]
		instance.save()
		return instance


# 用于补充ShopCartSerializer详情数据
class ShopCartDetailSerializer(serializers.ModelSerializer):
	'''
	购物车商品详情信息
	'''
	# 一个购物车对应一个商品
	goods = GoodsSerializer(many=False, read_only=True)
	class Meta:
		model = ShoppingCart
		fields = ("goods", "nums")



class OrderGoodsSerialzier(serializers.ModelSerializer):
	'''
	订单商品基本信息
	'''
	# 只序列化商品id，其他字段不序列化
	goods = GoodsSerializer(many=False)

	class Meta:
		model = OrderGoods
		fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
	'''
	商品订单详情
	'''
	goods = OrderGoodsSerialzier(many=True)

	# SerializerMethodField：https://blog.csdn.net/kongxx/article/details/50042579
	# 支付订单的url，不是直接保存在数据表中，因为由很多信息构成，所以查询时使用AliPay类配置获得
	alipay_url = serializers.SerializerMethodField(read_only=True)
	def get_alipay_url(self, obj):
		alipay = AliPay(
			appid="2018091300517456",
			app_notify_url="http://47.104.158.4:8000/alipay/return/",
			app_private_key_path=private_key_path,
			alipay_public_key_path=ali_pub_key_path,
			debug=True,
			return_url="http://47.104.158.4:8000/alipay/return/"
		)

		url = alipay.direct_pay(
			subject=obj.order_sn,
			out_trade_no=obj.order_sn,
			total_amount=obj.order_mount,
		)
		re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

		return re_url
	
	class Meta:
		model = OrderInfo
		fields = "__all__"




class OrderSerializer(serializers.ModelSerializer):
	'''
	商品订单信息
	'''
	user = serializers.HiddenField(
		default=serializers.CurrentUserDefault()
	)

	# 下面字段因为不能从post提供，所以需要指明read_only=True
	order_sn = serializers.CharField(read_only=True)

	# 交易过程中生成
	pay_status = serializers.CharField(read_only=True)
	pay_type = serializers.CharField(read_only=True)

	# 支付宝交易时生成
	trade_no = serializers.CharField(read_only=True)
	# 微信支付交易时生成
	nonce_str = serializers.CharField(read_only=True)

	pay_time = serializers.DateTimeField(read_only=True)

	# 支付订单的url
	alipay_url = serializers.SerializerMethodField(read_only=True)
	def get_alipay_url(self, obj):
		alipay = AliPay(
			appid="2018091300517456",
			app_notify_url="http://47.104.158.4:8000/alipay/return/",
			app_private_key_path=private_key_path,
			alipay_public_key_path=ali_pub_key_path,
			debug=True,
			return_url="http://47.104.158.4:8000/alipay/return/"
		)

		url = alipay.direct_pay(
			subject=obj.order_sn,
			out_trade_no=obj.order_sn,
			total_amount=obj.order_mount,
		)
		re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

		return re_url

	def generate_order_sn(self):
		# 生成订单号（当前时间+userid+随机数）
		import time
		from random import Random

		random_ins = Random()
		order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
																									userid=self.context['request'].user.id,
																									ranstr=random_ins.randint(10,99))

		return order_sn

	def validate(self,attrs):
		# 当所以数据合法时，更新order_sn字段，然后保存到数据库中
		attrs['order_sn'] = self.generate_order_sn()
		return attrs

	class Meta:
		model = OrderInfo
		fields = "__all__"



