import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Chat,Group
from channels.db import database_sync_to_async

# Generic WebSocket Method........
class MyWebsocketConsumer(WebsocketConsumer):

    def connect(self):
        print("Websocket connected")
        print("Channel Layer...", self.channel_layer)
        print("Channel Name...", self.channel_name)
        self.group_name = self.scope['url_route']['kwargs']['groupkaname']
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name,
        )
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        print("Message received...", text_data)
        data = json.loads(text_data)
        message = data['msg']

        group=Group.objects.get(name=self.group_name)
        if self.scope['user'].is_authenticated:
            chat = Chat(
                content = data['msg'],
                group=group
            )
            chat.save()

            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type':'chat.message',
                    'message':message
                }
            )
        else:
            self.send(text_data=json.dumps({
                'msg':"Login Required"
            }))

    def chat_message(self,event):
        print("Event..",event)
        self.send(text_data=json.dumps({
            'msg':event['message']
        }))

    def disconnect(self, code):
        print("websocket disconnected...", code)


class MyAsyncWebsocketConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("Wbsocket Connect...")
        print("Channel Layer...", self.channel_layer)
        print("Channel Name...", self.channel_name)
        self.group_name = self.scope['url_route']['kwargs']['groupkaname']
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        print("Message received...", text_data)
        data = json.loads(text_data)
        message = data['msg']

        group=await database_sync_to_async(Group.objects.get)(name=self.group_name)
        if self.scope['user'].is_authenticated:
            chat = Chat(
                content = data['msg'],
                group=group
            )
            await database_sync_to_async(chat.save)()
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat.message',
                    'message': message
                }
            )
        else:
            await self.send(text_data=json.dumps({
                'msg':'login Required'
            }))

    async def chat_message(self, event):
            print("Event..", event)
            await self.send(text_data=json.dumps({
                'msg': event['message']
            }))


    async def disconnect(self, code):
        print("Websocket Disconnected...", code)
