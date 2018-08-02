# https://blog.csdn.net/l_vip/article/details/79156113
from rest_framework import serializers

from user_operation.models import UserFav

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
		fields = ("user","goods","id")
