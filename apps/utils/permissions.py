# 认证/权限/频率限制: https://www.cnblogs.com/huchong/p/8450353.html
# django自带权限介绍: https://juejin.im/post/5872eb4fac502e006463e0d0
# https://blog.csdn.net/guyunzh/article/details/80443512
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
	"""
	Object-level permission to only allow owners of an object to edit it.
	Assumes the model instance has an `owner` attribute.
	"""

	def has_object_permission(self, request, view, obj):
		# Read permissions are allowed to any request,
		# so we'll always allow GET, HEAD or OPTIONS requests.
		# GET/HEAD/OPTIONS默认所有人许可，不需要用户认证（ReadOnly，范围大放前面）
		if request.method in permissions.SAFE_METHODS:
			return True

		# Instance must have an attribute named `owner`.（IsOwner，范围小放后面）
		#obj相当于数据库中的model，这里要把owner改为我们数据库中的user
		return obj.user == request.user