from django.views.generic import View
from goods.models import Goods

import json

# 返回时需要指定content_type
from django.http import HttpResponse

from django.core import serializers
# 已指定返回类型，直接返回数据即可
from django.http import JsonResponse


class GoodsListView(View):
	def get(self,request):
		json_list = []
		
		goods = Goods.objects.all()

		"""
		当字段很多时，一个一个提取字段麻烦
		for good in goods:
			json_dict = {}
			json_dict['name'] = good.name
			json_dict['category'] = good.category.name
			json_dict['market_price'] = good.market_price
			json_list.append(json_dict)
		"""

		"""
		使用model_to_dict帮助序列化字段，但是图片和时间字段等不能被序列化，会报错
		from django.forms.models import model_to_dict
		for good in goods:
			json_dict = model_to_dict(good)
			json_list.append(json_dict)
		"""

		# return HttpResponse(json.dumps(json_list),content_type='application/json')

		# 字段序列化定死的,**不能重组**，图片路径是相对路径，没有补全
		json_data = serializers.serialize('json',goods)
		json_data = json.loads(json_data)
		
		return JsonResponse(json_data, safe=False)