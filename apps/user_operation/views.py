from rest_framework import viewsets,mixins

from user_operation.models import UserFav

from user_operation.serializers import UserFavSerializer

# Create your views here.


class UserFavViewset(viewsets.GenericViewSet, 
											mixins.ListModelMixin,     # 获取列表
											mixins.CreateModelMixin,   # 添加收藏
											mixins.DestroyModelMixin): # 取消收藏
    '''
    用户收藏
    '''
    queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer

