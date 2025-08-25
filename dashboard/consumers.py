import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DataUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("data_updates", self.channel_name) # type: ignore
        await self.accept()
    async def disconnect(self, code): 
        await self.channel_layer.group_discard("data_updates", self.channel_name) # type: ignore
        # return await super().disconnect(code)
    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return 
        await self.send("Roger! " + text_data, bytes_data)
    async def send_update(self, _):
        await self.send(json.dumps({"type": "product_updated"}))