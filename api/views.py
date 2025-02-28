from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import replace_value_type_webhook
from .serializers import ConversationSerializer, MessageSerializer
from .services import (create_open_conversation, get_specific_conversation, close_conversation, 
                       create_message, get_specific_conversation_by_id, 
                       get_messages_by_conversation_id, get_all_conversations, get_last_message_by_conversation_id
                       )

@api_view(['POST'])
def webhook_endpoint(request):

    data_request = request.data

    status_serializer = False
    if ("type"  in data_request) and isinstance(data_request["type"], str):
        if(data_request["type"] == "NEW_CONVERSATION" or data_request["type"] == "CLOSE_CONVERSATION"):
            new_type = replace_value_type_webhook(data_request["type"])
            data_request["type"] = new_type

            serializer = ConversationSerializer(data=request.data)
            status_serializer = serializer.is_valid()

            if status_serializer == True:
                resturn_specific_conversation = get_specific_conversation(data_request["data"]["id"])

                if resturn_specific_conversation["status"] == False and new_type == "OPEN":
                    result_create_conversation = create_open_conversation(data_request["data"]["id"])

                    if result_create_conversation["status"] == True:
                        return Response( {"message": "Success! The conversation has been successfully created."}, status=201 )
                    return Response( {"message": "Oops! Your conversation was not created."}, status=400 )
                    
                elif resturn_specific_conversation["status"] == True and resturn_specific_conversation["conversation_state"] == "OPEN":
                    result_close_conversation = close_conversation(data_request["data"]["id"])

                    if result_close_conversation["status"] == True:
                        return Response( {"message": "All right! The conversation has been closed successfully."}, status=200 )
                    return Response( {"message": "Error! Unable to close conversation."}, status=400 )
                
                return Response( {"message": "Sorry, but this conversation has now closed."})
                
            
            return Response(serializer.errors, status=400)

        elif(data_request["type"] == "NEW_MESSAGE"):
            serializer = MessageSerializer(data=request.data)
            status_serializer = serializer.is_valid()

            if status_serializer == True:
                conversation_id = data_request["data"]["conversation_id"]

                resturn_specific_conversation = get_specific_conversation(conversation_id)

                if resturn_specific_conversation["status"] == True and resturn_specific_conversation["conversation_state"] == "OPEN":
                    content = data_request["data"]["content"]
                    message_type = data_request["data"]["direction"]
                    timestamp = data_request["timestamp"]

                    result_create_message = create_message(content, conversation_id, message_type, timestamp)
                    
                    if result_create_message["status"] == True:
                        return Response( {"message": "Message sent! Message creation was successful."}, status=201 )
                    return Response( {"message": "Sorry! Unable to create message."}, status=400 )
                return Response( {"message": "Sorry, but this conversation has now closed or doesn't even exist."})
            
            return Response(serializer.errors, status=400)
        
        return Response( {"status": status_serializer} )
    return Response( {"message": "Sorry, you didn't provide the 'type' key or the value is not a string"}, status=404 )



@api_view(['GET'])
def conversation_endpoint(request, param_id):
    conversation_getted = get_specific_conversation_by_id(param_id)
    
    if conversation_getted["status"] == True:
        consversation = conversation_getted["value"]
        messages = get_messages_by_conversation_id( consversation["conversation_id"] )


        return Response( {"consversation": consversation, "message": messages} )
    return Response( {"error": "Not Found", "message": "The requested conversation was not found."}, status=404 )



@api_view(['GET'])
def get_all_conversations_endpoint(request):
    result_get_all_conversations = get_all_conversations()

    if result_get_all_conversations["status"] == True:
        return Response( result_get_all_conversations["value"] )
    
    return Response({"error": "Not Found", "message": result_get_all_conversations["message"]}, status=404 )



@api_view(['GET'])
def last_message_endpoint(request, conversation_id):
    result_last_message_by_conversation_id = get_last_message_by_conversation_id(conversation_id)

    if result_last_message_by_conversation_id["status"] == True:
        return Response( result_last_message_by_conversation_id["value"] )
    
    return Response( {"error": "Not Found", "message": result_last_message_by_conversation_id["message"] }, status=404 )



def home(request):
    return render(request, 'index.html')