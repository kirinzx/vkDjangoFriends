from rest_framework import generics, viewsets
from .models import Invite, Friend
from .serializers import InviteSerializer, FriendSerializer, FriendAcceptSerializer
from rest_framework.response import Response
from apps.userProfile.models import UserProfile
from rest_framework import status
from itertools import chain
class InviteFriend(viewsets.ViewSet):
    def create(self,request):
        
        fromUser = request.data.get("fromUser")
        toUser = request.data.get("toUser")

        if fromUser == toUser:
            return Response(data={"yourself":"You can't be your friend!"},status=status.HTTP_400_BAD_REQUEST)
        
        if Friend.objects.filter(user_1=fromUser,user_2=toUser).exists() or Friend.objects.filter(user_1=toUser,user_2=fromUser).exists():
            return Response(data={"alreadyFriends":"You are already friends!"},status=status.HTTP_400_BAD_REQUEST)
        
        if Invite.objects.filter(fromUser=fromUser,toUser=toUser).exists():
            return Response(data={"inviteExists":"Invite is already created!"},status=status.HTTP_400_BAD_REQUEST)
        
        if Invite.objects.filter(fromUser=toUser,toUser=fromUser).exists():
            Friend.objects.create(user_1=UserProfile.objects.get(id=fromUser),user_2=UserProfile.objects.get(id=toUser))
            Invite.objects.filter(fromUser=UserProfile.objects.get(id=toUser),toUser=UserProfile.objects.get(id=fromUser)).delete()
            return Response(data={"successInvite":"You are friends"})
        
        invite = Invite.objects.create(fromUser=UserProfile.objects.get(id=fromUser),toUser=UserProfile.objects.get(id=toUser))
        return Response(data={
            "id": invite.id,
            "fromUser": invite.fromUser.id,
            "toUser":invite.toUser.id,
        })



class ListInvites(generics.ListAPIView):
    serializer_class = InviteSerializer
    def get_queryset(self):
        try:
            return Invite.objects.filter(fromUser=self.request.data.get("fromUser"))
        except:
            return Invite.objects.filter(toUser=self.request.data.get("toUser"))


class ListFriends(viewsets.ViewSet):
    def list(self,request,user=None):
        print(list(chain(Friend.objects.filter(user_1=user),Friend.objects.filter(user_2=user))))
        serializer = FriendSerializer(list(chain(Friend.objects.filter(user_1=user),Friend.objects.filter(user_2=user))),many=True)
        return Response(serializer.data)
#доработать


class DeleteFriend(generics.DestroyAPIView):
    serializer_class = FriendSerializer
    queryset = Friend.objects.all()


class AcceptInvite(generics.CreateAPIView):
    serializer_class = FriendAcceptSerializer
    queryset = Friend.objects.all()

class GetStatus(viewsets.ViewSet):
    def retrieve(self,request,pk=None):
        if Invite.objects.filter(fromUser=pk,toUser=request.data['suspect']).exists():
            response = {"friendshipStatus":"Sended an invite"}
        elif Invite.objects.filter(toUser=pk,fromUser=request.data['suspect']).exists():
            response = {"friendshipStatus":"Got an invite"}
        elif Friend.objects.filter(user_1=pk,user_2=request.data['suspect']).exists() or Friend.objects.filter(user_2=pk).exists():
            response = {"friendshipStatus":"Friends"}
        else:
            response = {"friendshipStatus":None}
        return Response(data=response)
        
