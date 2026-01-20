import json
from channels.generic.websocket import AsyncWebsocketConsumer

class UnifiedConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 1. Grab the cottage_id from the URL
        self.cottage_id = self.scope['url_route']['kwargs']['cottage_id']
        self.user = self.scope["user"]
        
        # 2. Security Check (Optional but recommended)
        # You could verify here if self.user has access to self.cottage_id
        
        if self.user.is_authenticated:
            # 3. Create unique group names for THIS cottage
            self.sensor_group = f"sensors_group_{self.cottage_id}"
            self.task_group = f"tasks_group_{self.cottage_id}"
            self.note_group = f"notes_group_{self.cottage_id}"

            await self.channel_layer.group_add(self.sensor_group, self.channel_name)
            await self.channel_layer.group_add(self.task_group, self.channel_name)
            await self.channel_layer.group_add(self.note_group, self.channel_name)
            
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, 'sensor_group'):
            await self.channel_layer.group_discard(self.sensor_group, self.channel_name)
            await self.channel_layer.group_discard(self.task_group, self.channel_name)
            await self.channel_layer.group_discard(self.note_group, self.channel_name)

    async def sensor_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "sensor_update",
            "payload": event["data"]
        }))

    async def task_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "task_update",
            "payload": event["data"]
        }))


    async def note_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "note_update",
            "payload": event["data"]
        }))