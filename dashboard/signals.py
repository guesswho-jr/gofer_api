from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .views import product_created
from .serializer import ProductListSerailizer

@receiver(product_created)
# @receiver(post_save, sender=Product)
def notify_save(instance, **kwargs):
    channel_layer = get_channel_layer()
    # print(instance.images)
    data = ProductListSerailizer(instance).data
    async_to_sync(channel_layer.group_send)("data_updates", {"type": "send_update", "data": {"category": instance.category, "product": data}}) # type: ignore