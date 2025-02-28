from django.urls import path
from .views import webhook_endpoint, conversation_endpoint, get_all_conversations_endpoint, last_message_endpoint, home

urlpatterns = [
    path('webhook/', webhook_endpoint),
    path('conversations/<int:param_id>/', conversation_endpoint),
    path('get_all_conversationt/', get_all_conversations_endpoint),
    path('last_message/<str:conversation_id>/', last_message_endpoint),
    path('home/', home),
]