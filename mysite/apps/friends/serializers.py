from rest_framework.serializers import ModelSerializer
from .models import Invite, Friend
from rest_framework import serializers

class InviteSerializer(ModelSerializer):
    class Meta:
        model = Invite
        fields = ("fromUser","toUser",)

class FriendSerializer(ModelSerializer):
    class Meta:
        model = Friend
        fields = ("user_1","user_2",)