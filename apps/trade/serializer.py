from trade.models import ShoppingCart
from goods.models import Goods

from goods.serializers import GoodsSerializer

from rest_framework import serializers



class ShopCartSerializer(serializers.Serializer):
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