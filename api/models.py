from django.db import models


class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    conversation_id = models.CharField(max_length=255, unique=True)
    conversation_state = models.CharField(max_length=10)



class Message(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    conversation_id = models.CharField(max_length=255)
    message_type = models.CharField(
        max_length=8,
        choices=[('SENT', 'SENT'), ('RECEIVED', 'RECEIVED')]
    )
    timestamp = models.DateTimeField()
