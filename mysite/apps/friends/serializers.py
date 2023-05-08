from rest_framework.serializers import ModelSerializer
from .models import Friend
from rest_framework import serializers
from django.http import Http404

class FriendSerializer(ModelSerializer):
    class Meta:
        model = Friend
        fields = ("user_1","user_2",)

class FriendAcceptSerializer(ModelSerializer):
    class Meta:
        model = Friend
        fields = ("user_1","user_2",)
    def create(self, validated_data):
        if Invite.objects.filter(fromUser=validated_data['user_1'],toUser=validated_data['user_2']).exists():
            Friend.objects.create(**validated_data)
            Invite.objects.filter(fromUser=validated_data['user_1'],toUser=validated_data['user_2']).delete()
            return Friend(**validated_data)
        elif Invite.objects.filter(fromUser=validated_data['user_2'],toUser=validated_data['user_1']).exists():
            Friend.objects.create(**validated_data)
            Invite.objects.filter(fromUser=validated_data['user_2'],toUser=validated_data['user_1']).delete()
            return Friend(**validated_data)
        else:
            raise Http404
        