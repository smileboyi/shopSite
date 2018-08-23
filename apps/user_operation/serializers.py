# https://blog.csdn.net/l_vip/article/details/79156113
from rest_framework import serializers

from user_operation.models import UserFav,UserLeavingMessage,UserAddress
from goods.serializers import GoodsSerializer

from rest_framework.validators import UniqueTogetherValidator



class UserFavSerializer(serializers.ModelSerializer):
	'''
	用户收藏
	'''

	# HiddenField的值不依靠输入，而需要设置默认的值，也不会显式返回给用户
	# 默认user就是当前登录用户，不需要前端用户post过来
	user = serializers.HiddenField(
		# 根据用户场景自行赋值
		default = serializers.CurrentUserDefault()
	)

	class Meta:
		validators = [
			UniqueTogetherValidator(
				queryset = UserFav.objects.all(),
				# 商品收藏动作是唯一的，不能收藏多次：user id + goods id
				fields=('user', 'goods'),
				# message的信息可以自定义
				message="已经收藏"
			)
		]
		model = UserFav
		# 收藏的时候需要返回商品的id，因为取消收藏的时候必须知道商品的id是多少
		fields = ("user","goods","id")



class UserFavDetailSerializer(serializers.ModelSerializer):
	'''
	用户收藏详情
	'''

	# 通过商品id获取收藏的商品，需要嵌套商品的序列化
	goods = GoodsSerializer()
	class Meta:
		model = UserFav
		fields = ("goods", "id")




class LeavingMessageSerializer(serializers.ModelSerializer):
	'''
	用户留言
	'''
	# 获取当前登录的用户
	user = serializers.HiddenField(
		default=serializers.CurrentUserDefault()
	)
	#read_only:只返回，post时候可以不用提交，format：格式化输出
	add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

	class Meta:
		model = UserLeavingMessage
		fields = ("user", "message_type", "subject", "message", "file", "id" ,"add_time")




class AddressSerializer(serializers.ModelSerializer):
	user = serializers.HiddenField(
		default=serializers.CurrentUserDefault()
	)
	add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
	class Meta:
		model = UserAddress
		fields = ("id", "user", "province", "city", "district", "address", "signer_name", "add_time", "signer_mobile")