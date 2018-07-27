# https://blog.csdn.net/mr_sunqq/article/details/78841845
# import django.shortcuts

from rest_framework.views import APIView
from rest_framework.response import Response

from goods.serializers import GoodsSerializer

from rest_framework import mixins
from rest_framework import generics

from .models import Goods
# Create your views here.


class GoodsListView(APIView):
	'商品列表页'
	def get(self,request,format=None):
		goods = Goods.objects.all()
		goods_serializer = GoodsSerializer(goods,many=True)

		return Response(goods_serializer.data)


# ListAPIView继承了APIView
class GoodsListView(generics.ListAPIView):
	'商品列表页'
	queryset = Goods.objects.all()
	serializer_class = GoodsSerializer

	def get(self,request,*args,**kwargs):
		return self.list(request,*args,**kwargs)
