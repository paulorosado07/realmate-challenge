from rest_framework import serializers

class ConversationDataSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255)

class ConversationSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=50)
    timestamp = serializers.DateTimeField()
    data = ConversationDataSerializer()
    


class MessageDataSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255)
    direction = serializers.ChoiceField(choices=["RECEIVED", "SENT"])
    content = serializers.CharField(max_length=None)
    conversation_id = serializers.CharField(max_length=255)

class MessageSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=50)
    timestamp = serializers.DateTimeField()
    data = MessageDataSerializer()
