from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


# -------------------------
# Conversation ViewSet
# -------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().prefetch_related("participants", "messages")
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants.
        Expects a list of user IDs in request.data["participants"]
        """
        participant_ids = request.data.get("participants", [])
        if not participant_ids:
            return Response({"error": "Participants are required"}, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        users = User.objects.filter(id__in=participant_ids)
        conversation.participants.set(users)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# -------------------------
# Message ViewSet
# -------------------------
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().select_related("sender", "conversation")
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Send a new message in a conversation.
        Expects: conversation (id), sender (id), message_body
        """
        conversation_id = request.data.get("conversation")
        sender_id = request.data.get("sender")
        body = request.data.get("message_body")

        if not conversation_id or not sender_id or not body:
            return Response(
                {"error": "conversation, sender, and message_body are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = get_object_or_404(Conversation, id=conversation_id)
        sender = get_object_or_404(User, id=sender_id)

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=body
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
