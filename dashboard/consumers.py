import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DataUpdateConsumer(AsyncWebsocketConsumer):
    async def __call__(self, scope, receive, send):
        # print(await receive())
        return await super().__call__(scope, receive, send)
    async def connect(self):
        print(self.scope)
        if self.scope["ws_forbidden"]:
            await self.close(700)
        await self.channel_layer.group_add("data_updates", self.channel_name) # type: ignore
        await self.accept()
    async def disconnect(self, code): 
        await self.channel_layer.group_discard("data_updates", self.channel_name) # type: ignore
    async def send_update(self, event):
        await self.send(json.dumps({"type": "product_updated", **event["data"]}))