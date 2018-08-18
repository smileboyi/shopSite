from django.apps import AppConfig

# https://docs.djangoproject.com/en/1.10/ref/applications/
# AppConfig这个基类描述了一个Django应用以及它的配置信息
# 定义了XyzConfig后，使用不再是AppConfig，而是XyzConfig
# 需在配置文件的INSTALL_APPS项中，把your app改为your app.MyConfig，或者在你的app的init.py定义default_app_config = ‘your app.MyConfig’

class UsersConfig(AppConfig):
	name = 'users'
	# app名字后台显示中文
	verbose_name = "用户管理"

	def ready(self):
		import users.signals