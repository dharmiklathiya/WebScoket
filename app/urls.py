from . import views
from django.urls import path

urlpatterns = [
    # path('<str:group_name>/',views.index),
    # path('<str:group_name>/',views.index1), ## Generic WebSocket Method........
    path('<str:group_name>/',views.index2), ## JsonWebsocketConsumer Method....
]
