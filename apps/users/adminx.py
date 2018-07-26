import xadmin
from xadmin import views
from .models import VerifyCode

"""
不是使用默认的后台管理，是使用的xadmin后台
使用情况和admin一样的操作
"""
class BaseSetting(object):
	#添加主题功能
	enable_themes = True
	# use_bootswatch无效问题：https://my.oschina.net/u/2396236/blog/1083251
	use_bootswatch = True


class GlobalSettings(object):
	#全局配置，后台管理标题和页脚
	site_title = "shopSite后台管理"
	site_footer = "http://www.cnblogs.com/derek1184405959/"

	#菜单收缩，菜单名就是app.py中设置的verbose_name，选项名就是模型中设置的verbose_name
	menu_style = "accordion"


class VerifyCodeAdmin(object):
	list_display = ['code', 'mobile', "add_time"]



"""
xadmin.sites.AlreadyRegistered: The model UserProfile is already registered
需要先注销，然后再注册：
xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile, UserProfileAdmin)
"""

xadmin.site.register(VerifyCode, VerifyCodeAdmin)

# 基于BaseAdminView（base.py中，和TemplateView类似，通过as_view方法使用）进行后台管理视图定制
# 只能在一处定制BaseAdminView和CommAdminView，此处定制了，其他地方再定制会报错
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
