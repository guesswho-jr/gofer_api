from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Product

@receiver(post_save, sender=Product)
def notify_save(*args,**kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("data_updates", {"type": "send_update"}) # type: ignore