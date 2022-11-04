from rest_framework import serializers
from .models import Mail


class MailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mail
        fields = [
            "message_id",
            "thread_id",
            "snippet",
        ]