# https://django-filter.readthedocs.io/en/master/guide/usage.html#the-filter
import django_filters

from django.db.models import Q

from .models import Goods


# 自定义过滤类需要继承FilterSet类
class GoodsFilter(django_filters.rest_framework.FilterSet):
	'''商品过滤的类'''
	
	# 自定义过滤字段和过滤行为
	pricemin = django_filters.NumberFilter(field_name="shop_price", lookup_expr='gt', help_text='最低价格')
	pricemax = django_filters.NumberFilter(field_name="shop_price", lookup_expr='lt', help_text='最高价格')

	# 外键字段
	top_category = django_filters.NumberFilter(label="category", method='top_category_filter')
	def top_category_filter(self, queryset, name, value):
		# 不管当前点击的是一级分类二级分类还是三级分类，都能找到。
		return queryset.filter(Q(category_id=value) | 
													Q(category__parent_category_id=value) | 
													Q(category__parent_category__parent_category_id=value))

	class Meta:
		model = Goods
		# 前2个是自定义范围过滤字段，后2个是自带布尔字段；外键字段不需要列出
		fields = ['pricemin','pricemax','is_hot','is_new']