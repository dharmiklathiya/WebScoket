from channels.consumer import SyncConsumer,AsyncConsumer
from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer
import json
from .models import Chat,Group
from channels.db import database_sync_to_async
class MySyncConsumer(SyncConsumer):

    def websocket_connect(self,event):
        print("websocket connected...",event)
        print(("Channel Layer...",self.channel_layer))
        print(("Channel Name...",self.channel_name))

        self.group_name = self.scope['url_route']['kwargs']['groupkaname']
        print("Group Name..",self.group_name)

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.send({
            'type':'websocket.accept',
        })

    def websocket_receive(self,event):
        print("websocket received...")
        print(event['text'])

        data = json.loads(event['text'])
        print("Data..",data['msg'])
        print(self.scope['user'])

        group=Group.objects.get(name=self.group_name)
        if self.scope['user'].is_authenticated:
            chat = Chat(
                content = data['msg'],
                group = group
            )
            chat.save()
            data['user']=self.scope['user'].username
            print("complate data..",data)

            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                'type':'chat.message',
                'message':json.dumps(data)
                }
            )
        else:
            self.send({
                'type':'websocket.send',
                'text':json.dumps({"msg":"Login Required","user":"gust"})
            })

    def chat_message(self,event):
        print(event['message'])
        self.send({
            'type':'websocket.send',
            'text':event['message']
        })

    def websocket_disconnect(self,event):
        print("websocket disconnected...",event)
        print(("Channel Layer...", self.channel_layer))
        print(("Channel Name...", self.channel_name))
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
        raise StopConsumer()

class MyAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self,event):
        print("websocket connected...",event)
        print(("Channel Layer...",self.channel_layer))
        print(("Channel Name...",self.channel_name))

        self.group_name = self.scope['url_route']['kwargs']['groupkaname']

        print("Group Name..", self.group_name)

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.send({
            'type':'websocket.accept',
        })

    async def websocket_receive(self,event):
        print("websocket received...")
        print(event['text'])
        data = json.loads(event['text'])
        print("Data..", data['msg'])

        group = await database_sync_to_async(Group.objects.get)(name=self.group_name)
        if self.scope['user'].is_authenticated:
            chat = Chat(
                content=data['msg'],
                group=group
            )
            data['user'] = self.scope['user'].username
            print("complate data..", data)

            await database_sync_to_async(chat.save)()
            await self.channel_layer.group_send(
                self.group_name,
                {
                'type':'chat.message',
                'message':json.dumps(data)
                }
            )
        else:
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps({"msg": "Login Required", "user": "gust"})
            })

    async def chat_message(self,event):
        print(event['message'])
        await self.send({
            'type':'websocket.send',
            'text':event['message']
            })

    async def websocket_disconnect(self,event):
        print("websocket disconnected...",event)
        print(("Channel Layer...", self.channel_layer))
        print(("Channel Name...", self.channel_name))
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        raise StopConsumer()