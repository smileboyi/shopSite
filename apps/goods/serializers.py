from rest_framework import serializers

from .models import Goods,GoodsCategory,GoodsImage

"""
class GoodsSerializer(serializers.Serializer):
	# 列出要序列化的字段，展示给前端，字段名和模型里定义的字段名一致
	name = serializers.CharField(required=True,max_length=100)
	click_num = serializers.IntegerField(default=0)

	# 图片字段按ImageField()反序列化，自动补全地址
	goods_front_image = serializers.ImageField()
"""

"""
# 当要序列化所有字段时，这样写
class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = GoodsCategory
		fields = "__all__"
"""


class CategorySerializer3(serializers.ModelSerializer):
	'''
	三级分类
	'''
	class Meta:
		model = GoodsCategory
		fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
	'''
	二级分类
	'''
	# 在parent_category字段中定义的related_name="sub_cat"
	# 可以通过三级分类id获取列表数据
	sub_cat = CategorySerializer3(many=True)
	class Meta:
		model = GoodsCategory
		fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
	'''
	商品一级类别序列化
	'''
	# 可以通过二级分类id获取列表数据
	sub_cat = CategorySerializer2(many=True)
	class Meta:
		model = GoodsCategory
		fields = "__all__"



class GoodsImageSerializer(serializers.ModelSerializer):
	'''
	轮播图
	'''
	class Meta:
		model = GoodsImage
		fields = ("image",)



class GoodsSerializer(serializers.ModelSerializer):
	'''
	商品列表序列化
	'''
	# 覆盖外键字段，返回嵌套信息。不覆盖默认返回主表主键
	# category为反向引用，不会被fields默认包含，所以需要添加显示字段
	category = CategorySerializer()

	# 也是一个外键，如果要序列化所有字段加上many=True
	images = GoodsImageSerializer(many=True)
	class Meta:
		model = Goods
		fields = "__all__"



