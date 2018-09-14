from rest_framework import serializers

from goods.models import Goods,GoodsCategory,GoodsImage,Banner,GoodsCategoryBrand,IndexAd,HotSearchWords

from django.db.models import Q



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



class BannerSerializer(serializers.ModelSerializer):
	'''
	轮播图
	'''
	class Meta:
		model = Banner
		fields = "__all__"



class BrandSerializer(serializers.ModelSerializer):
	'''
	大类下面的宣传商标
	'''
	class Meta:
		model = GoodsCategoryBrand
		fields = "__all__"



class IndexCategorySerializer(serializers.ModelSerializer):
	'''
	首页商品分类数据:
		商品商标（多个）
		大类下的二级类
		广告商品
		所有商品
	'''
	# 某个大类的商标，可以有多个商标，一对多的关系
	brands = BrandSerializer(many=True)

	# 取二级商品分类
	sub_cat = CategorySerializer2(many=True)

	# 广告商品
	ad_goods = serializers.SerializerMethodField()
	def get_ad_goods(self, obj):
		goods_json = {}
		ad_goods = IndexAd.objects.filter(category_id=obj.id, )
		if ad_goods:
			# 取到这个商品id（obj.id唯一，所以[0]）,不能获取商品信息
			good_ins = ad_goods[0].goods
			# 通过商品id取商品信息
			# 嵌套serializer必须添加一个参数context（上下文request）,serializer返回的时候一定要加 “.data” ，这样才是json数据
			goods_json = GoodsSerializer(good_ins, many=False, context={'request': self.context['request']}).data

		return goods_json

	# good有一个外键category，但这个外键指向的是三级类，直接反向通过外键category（三级类），取某个大类下面的商品是取不出来的
	goods = serializers.SerializerMethodField()
	def get_goods(self, obj):
		# 将这个商品相关父类子类等都可以进行匹配
		all_goods = Goods.objects.filter(Q(category_id=obj.id) | 
																			Q(category__parent_category_id=obj.id) | 
																			Q(category__parent_category__parent_category_id=obj.id))
		goods_serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context['request']})

		return goods_serializer.data

	class Meta:
		model = GoodsCategory
		fields = "__all__"




class HotWordsSerializer(serializers.ModelSerializer):
	'''
	热搜词
	'''
	class Meta:
		model = HotSearchWords
		fields = "__all__"