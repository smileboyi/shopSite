# https://blog.csdn.net/mr_sunqq/article/details/78841845
# import django.shortcuts

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets

from rest_framework.pagination import PageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from goods.serializers import GoodsSerializer,CategorySerializer,BannerSerializer,IndexCategorySerializer,HotWordsSerializer

from goods.models import Goods,GoodsCategory,Banner,GoodsCategory,HotSearchWords

from goods.filters import GoodsFilter

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
class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
	'''
	list:
		商品列表，分页，搜索，过滤，排序
	retrieve:
		获取商品详情
	'''
	# 查询集，这里必须要定义一个默认的排序,否则会报错
	queryset = Goods.objects.all().order_by('id')

	# 序列化
	serializer_class = GoodsSerializer

	# 分页
	pagination_class = GoodsPagination

	# 使用后端过滤，使用搜索过滤和排序过滤
	filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
	# 可以搜索的字段
	"""
	'^' ：以xx字符串开始搜索
	'=' ：完全匹配
	'@' ：全文搜索（目前只支持Django的MySQL后端）
	'$' ：正则表达式搜索
	"""
	search_fields = ('=name', 'goods_brief', 'goods_desc')
 	# 需要排序的字段
	ordering_fields = ('sold_num', 'shop_price')

	# 使用前端过滤，表单组合
	filter_class = GoodsFilter

	# 当用户进入详情页时表示商品点击数加1
	def retrieve(self, request, *args, **kwargs):
		instance = self.get_object()
		instance.click_num += 1
		instance.save()
		serializer = self.get_serializer(instance)
		
		return Response(serializer.data)



class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
	'''
	商品分类列表数据(get)
	'''
	queryset = GoodsCategory.objects.filter(category_type=1)
	serializer_class = CategorySerializer




class BannerViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
	'''
	首页轮播图
	'''
	queryset = Banner.objects.all().order_by('index')
	serializer_class = BannerSerializer



class IndexCategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
	'''
	首页商品分类数据
	'''
	# 获取is_tab=True（导航栏）里面的分类下的商品数据
	queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["生鲜食品", "酒水饮料"])
	serializer_class = IndexCategorySerializer



class HotSearchsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
	'''
	热搜词
	'''
	# 搜索越多越在前面
	queryset = HotSearchWords.objects.all().order_by("-index")
	serializer_class = HotWordsSerializer