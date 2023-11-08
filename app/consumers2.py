from channels.generic.websocket import JsonWebsocketConsumer,AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Chat,Group
from channels.db import database_sync_to_async

# JsonWebsocketConsumer Method....
class MyJsonWebsocketConsumer(JsonWebsocketConsumer):

    def connect(self):
        print("Websocket Connect..")
        print("Channel Layer..",self.channel_layer)
        print("Channel Name..",self.channel_name)
        self.group_name = self.scope['url_route']['kwargs']['groupkaname']
        print("Group Name..",self.group_name)
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def receive_json(self, content, **kwargs):
        print("Message Received..",content)
        group = Group.objects.get(name= self.group_name)
        if self.scope['user'].is_authenticated:
            chat = Chat(
                content = content['msg'],
                group=group
            )
            chat.save()

            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type':'chat.message',
                    'message':content['msg']
                }
            )
        else:
            self.send_json({
                'message':'Login Required'
            })

    def chat_message(self,event):
        self.send_json({
            'message':event['message']
        })


    def disconnect(self, code):
        print("Websocket Disconnected...",code)
        print("Channel Layer..", self.channel_layer)
        print("Channel Name..", self.channel_name)
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

class MyAsyncJsonWebsocketConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        print("Webscoket Connect..")
        print("Channel Layer..", self.channel_layer)
        print("Channel Name..", self.channel_name)
        self.group_name = self.scope['url_route']['kwargs']['groupkaname']
        print("Group Name..", self.group_name)
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def receive_json(self, content, **kwargs):
        print("Message Received..",content)
        group=await database_sync_to_async(Group.objects.get)(name=self.group_name)
        if self.scope['user'].is_authenticated:
            chat = Chat(
                content = content['msg'],
                group=group
            )
            await database_sync_to_async(chat.save)()
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat.message',
                    'message': content['msg']
                }
            )
        else:
            await self.send_json({
                'message':'Login Required'
            })

    async def chat_message(self, event):
            await self.send_json({
                'message': event['message']
            })

    async def disconnect(self, code):
        print("Websocket Disconnected..",code)
        print("Channel Layer..", self.channel_layer)
        print("Channel Name..", self.channel_name)
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
