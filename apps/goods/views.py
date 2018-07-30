# https://blog.csdn.net/mr_sunqq/article/details/78841845
# import django.shortcuts

from rest_framework.views import APIView
from rest_framework.response import Response

from goods.serializers import GoodsSerializer

from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets

from rest_framework.pagination import PageNumberPagination

from .models import Goods
# Create your views here.


class GoodsPagination(PageNumberPagination):
	'''
	商品列表自定义分页
	'''
	#默认每页显示的个数
	page_size = 10
	#可以动态改变每页显示的个数
	page_size_query_param = 'page_size'
	#页码参数
	page_query_param = 'page'
	#最多能显示多少页
	max_page_size = 100




"""
只使用APIView,需手动写get方法,跟基于方法的视图差别不多
class GoodsListView(APIView):
	def get(self,request,format=None):
		goods = Goods.objects.all()
		goods_serializer = GoodsSerializer(goods,many=True)

		return Response(goods_serializer.data)
"""


"""
# ListAPIView继承了APIView,提供了get方法
class GoodsListView(generics.ListAPIView):
	'商品列表页'
	queryset = Goods.objects.all()
	serializer_class = GoodsSerializer

	# 分页
	pagination_class = GoodsPagination

"""


# ViewSet类与View类其实几乎是相同的,但提供的是read或update这些操作,而不是get或put等HTTP动作。
# 同时，ViewSet为我们提供了默认的URL结构, 使得我们能更专注于API本身。
class GoodsListViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
	'商品列表页'
	#这里必须要定义一个默认的排序,否则会报错
	queryset = Goods.objects.all().order_by('id')
	serializer_class = GoodsSerializer

	pagination_class = GoodsPagination
