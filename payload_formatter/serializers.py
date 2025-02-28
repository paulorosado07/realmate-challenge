from rest_framework import serializers

class CloseConversationSerializer(serializers.Serializer):
    conversation_id = serializers.UUIDField()


class MessageSerializer(serializers.Serializer):
    conversation_id = serializers.UUIDField()
    content = serializers.CharField()
