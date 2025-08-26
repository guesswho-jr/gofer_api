import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DataUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("data_updates", self.channel_name) # type: ignore
        await self.accept()
    async def disconnect(self, code): 
        await self.channel_layer.group_discard("data_updates", self.channel_name) # type: ignore
    async def send_update(self, event):
        await self.send(json.dumps({"type": "product_updated", "data": event["data"]}))