from django.urls import path
from . import consumers1

# Generic WebSocket Using Method.......

websocket_urlpatterns = [
    path('ws/wsc/<str:groupkaname>/',consumers1.MyWebsocketConsumer.as_asgi()),
    path('ws/awsc/<str:groupkaname>/',consumers1.MyAsyncWebsocketConsumer.as_asgi()),
]