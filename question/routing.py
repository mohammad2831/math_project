from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/score/<int:user_id>/', consumers.ScoreConsumer.as_asgi()),
]
