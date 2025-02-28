from django.urls import path
from .views import open_conversation, close_conversation, send_message, receive_message

urlpatterns = [
    path('open_conversation/', open_conversation),
    path('close_conversation/', close_conversation),
    path('send_message/', send_message),
    path('receive_message/', receive_message),
]