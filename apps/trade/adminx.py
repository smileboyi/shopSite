import xadmin
from .models import ShoppingCart, OrderInfo, OrderGoods


class ShoppingCartAdmin(object):
	list_display = ["user", "goods", "nums", ]



class OrderInfoAdmin(object):
	list_display = ["user", "order_sn",  "trade_no", "pay_status", "post_script", "order_mount",
									"order_mount", "pay_time", "add_time"]

	# 使用了关联,就不用单独一个管理器注册了
	class OrderGoodsInline(object):
			model = OrderGoods
			exclude = ['add_time', ]
			extra = 1
			style = 'tab'

	# 父子表的情况。编辑父表之后，再打开子表编辑，而且子表只能一条一条编辑，比较麻烦。
	# 在外键关联这种情况，我们也可以将其放在同一个编辑界面中进行处理。
	inlines = [OrderGoodsInline, ]



xadmin.site.register(ShoppingCart, ShoppingCartAdmin)
xadmin.site.register(OrderInfo, OrderInfoAdmin)