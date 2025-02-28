from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import generate_timestamp, generate_conversation_id, generate_new_message, get_base_url
from .serializers import CloseConversationSerializer, MessageSerializer

import requests

@api_view(['POST'])
def open_conversation(request):

    url = request.build_absolute_uri()
    domain  = get_base_url(url)

    timestamp = generate_timestamp()
    conversation_id = generate_conversation_id()
    
    new_conversation = {
        "type": "NEW_CONVERSATION",
        "timestamp": timestamp,
        "data": {
            "id": conversation_id
        }
    }
    requests.post(f"{domain}/webhook/", json=new_conversation)
    return Response( new_conversation )



@api_view(['POST'])
def close_conversation(request):
    url = request.build_absolute_uri()
    domain  = get_base_url(url)
    
    serializer = CloseConversationSerializer(data=request.data)
    if serializer.is_valid():        
        timestamp = generate_timestamp()
        conversation_id = request.data["conversation_id"]
        close_conversation = {
            "type": "CLOSE_CONVERSATION",
            "timestamp": timestamp,
            "data": {
                "id": conversation_id
            }
        }
        requests.post(f"{domain}/webhook/", json=close_conversation)
        return Response( close_conversation )
    return Response(serializer.errors, status=400)
    


@api_view(['POST'])
def send_message(request):
    url = request.build_absolute_uri()
    domain  = get_base_url(url)

    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():        
        content = serializer.validated_data.get('content')
        conversation_id = request.data["conversation_id"]
        message_sented = generate_new_message("SENT", content, conversation_id)
        requests.post(f"{domain}/webhook/", json=message_sented)
        return Response( message_sented )
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def receive_message(request):
    url = request.build_absolute_uri()
    domain  = get_base_url(url)
    
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():        
        content = serializer.validated_data.get('content')
        conversation_id = request.data["conversation_id"]
        message_received = generate_new_message("RECEIVED", content, conversation_id)
        requests.post(f"{domain}/webhook/", json=message_received)
        return Response( message_received )
    return Response(serializer.errors, status=400)