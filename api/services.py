from .models import Conversation, Message
from django.forms.models import model_to_dict

def create_open_conversation(param_conversation_id):
    result_return = {"status": False}

    try:
        conversation = Conversation(conversation_id=param_conversation_id, conversation_state="OPEN")
        conversation.save()
        result_return["status"] = True
    except Exception as e:
        print(f"Error inserting: {e}")
    
    return result_return


def get_specific_conversation(param_conversation_id):
    result_return = {"status": False, "conversation_state": "CLOSED"}

    try:
        conversation = Conversation.objects.get(conversation_id__iexact=param_conversation_id)
        result_return["status"] = True
        result_return["conversation_state"] = conversation.conversation_state
    except:
        pass
    return result_return

def get_specific_conversation_by_id(param_id):
    result_return = {"status": False, "value": {}}

    try:
        conversation = model_to_dict( Conversation.objects.get(id=param_id) )
        result_return["status"] = True
        result_return["value"] = conversation
    except:
        pass
    return result_return


def get_all_conversations():
    result_return = {"status": False, "value": []}
    
    try:
        conversation = list(Conversation.objects.values())
        result_return["status"] = True
        result_return["value"] = conversation
    except Exception as e:
        result_return["message"] = "Sorry, but it was not possible to retrieve the conversations in this request."
        print(f"Error Get Data: {e}")

    return result_return

def close_conversation(param_conversation_id):
    result_return = {"status": False}
    try:
        Conversation.objects.filter(conversation_id=param_conversation_id).update(conversation_state="CLOSED")
        result_return["status"] = True
    except Exception as e:
        print(f"Error update: {e}")
    
    return result_return

def create_message(param_content, param_conversation_id, param_message_type, param_timestamp):
    result_return = {"status": False}
    try:
        message = Message(content=param_content, conversation_id=param_conversation_id, message_type=param_message_type, timestamp=param_timestamp)
        message.save()
        result_return["status"] = True
    except Exception as e:
        print(f"Error update: {e}")
    
    return result_return


def get_messages_by_conversation_id(param_conversation_id):
    messages_list = []
    try:
        messages = Message.objects.filter(conversation_id__exact=param_conversation_id).values()
        messages_list = list(messages)
    except Exception as e:
        print(f"Erro: {e}")
    return messages_list



def get_last_message_by_conversation_id(param_conversation_id):
    result_return = {"status": False, "value": {}}

    try:
        last_message = Message.objects.filter(conversation_id__exact=param_conversation_id).order_by('-id').values().first()
        
        
        if last_message != None:
            result_return["status"] = True
            result_return["value"] = last_message
    except Exception as e:
        
        print(f"Erro: {e}")

    if result_return["status"] == False:
        result_return["message"] = "Sorry, but it was not possible to retrieve the last message in this request."
    
    return result_return