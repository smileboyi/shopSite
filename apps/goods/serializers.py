from rest_framework import serializers

from .models import Goods,GoodsCategory


class GoodsSerializer(serializers.Serializer):
	# 列出要序列化的字段，展示给前端，字段名和模型里定义的字段名一致
	name = serializers.CharField(required=True,max_length=100)
	click_num = serializers.IntegerField(default=0)

	# 图片字段按ImageField()反序列化，自动补全地址
	goods_front_image = serializers.ImageField()



# 当要序列化所有字段时，这样写
class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = GoodsCategory
		fields = "__all__"



class GoodsSerializer(serializers.ModelSerializer):
	# 覆盖外键字段，返回嵌套信息。不覆盖默认返回主表主键
	category = CategorySerializer()
	class Meta:
		model = Goods
		fields = '__all__'



