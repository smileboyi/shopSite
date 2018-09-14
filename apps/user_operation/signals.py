from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from user_operation.models import UserFav

# 商品收藏数信号量
@receiver(post_save, sender=UserFav)
def create_UserFav(sender, instance=None, created=False, **kwargs):
	if created:
		goods = instance.goods
		goods.fav_num += 1
		goods.save()

@receiver(post_delete, sender=UserFav)
def delete_UserFav(sender, instance=None, created=False, **kwargs):
	goods = instance.goods
	goods.fav_num -= 1
	goods.save()



