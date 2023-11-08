from django.urls import path
from . import consumers2

# JsonWebsocketConsumer Method....

websocket_urlpatterns = [
    path('ws/jwc/<str:groupkaname>/',consumers2.MyJsonWebsocketConsumer.as_asgi()),
    path('ws/ajwc/<str:groupkaname>/',consumers2.MyAsyncJsonWebsocketConsumer.as_asgi()),
]