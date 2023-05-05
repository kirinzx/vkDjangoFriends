from django.shortcuts import render
from rest_framework import generics
from .models import Invite, Friend
from .serializers import InviteSerializer, FriendSerializer


class InviteFriend(generics.CreateAPIView):
    queryset = Invite.objects.all()
    serializer_class = InviteSerializer


class ListInvites(generics.ListAPIView):
    serializer_class = InviteSerializer
    def get_queryset(self):
        queryset = Invite.objects.filter(fromUser=self.request.data.get("fromUser"))
        if len(queryset) == 0:
            return Invite.objects.filter(toUser=self.request.data.get("toUser"))
        return queryset

class ListFriends(generics.ListAPIView):
    queryset = Friend.objects.all()
    lookup_field = "user_1"
    serializer_class = FriendSerializer


class DeleteFriend(generics.DestroyAPIView):
    serializer_class = FriendSerializer
    queryset = Friend.objects.all()


# Принятие инвайта - передаем toUser, fromUser, потом сохраняем в таблицу friends эти поля
