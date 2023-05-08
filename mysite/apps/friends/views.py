from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Friend
from .serializers import FriendSerializer
from rest_framework.response import Response
from apps.userProfile.models import UserProfile
from apps.userProfile.serializers import UserProfileSerializer
from rest_framework import status
from itertools import chain


class CreateInvite(APIView):

    def post(self, request):

        fromUser = request.data.get("inviter")
        toUser = request.data.get("accepter")

        if not UserProfile.objects.filter(id=fromUser).exists() or not UserProfile.objects.filter(id=toUser).exists():
            return Response(data={"detail":"Not found"},status=status.HTTP_404_NOT_FOUND)

        if fromUser == toUser:
            return Response(data={"detail": "You can't be your friend!"}, status=status.HTTP_400_BAD_REQUEST)

        if Friend.objects.filter(user_1=fromUser, user_2=toUser, status=2).exists() or Friend.objects.filter(user_1=toUser, user_2=fromUser, status=2).exists():
            return Response(data={"detail": "You are already friends!"}, status=status.HTTP_400_BAD_REQUEST)

        if Friend.objects.filter(user_1=fromUser, user_2=toUser, status=0).exists():
            return Response(data={"detail": "Invite is already created!"}, status=status.HTTP_400_BAD_REQUEST)

        if Friend.objects.filter(user_1=toUser, user_2=fromUser, status=0).exists():
            Friend.objects.filter(
                user_1=toUser, user_2=fromUser, status=0).update(status=2)
            return Response(data={"successInvite": "You are friends"})

        invite = Friend.objects.create(user_1=UserProfile.objects.get(
            id=fromUser), user_2=UserProfile.objects.get(id=toUser), status=0)
        serializer = FriendSerializer(invite)

        return Response(data=serializer.data)
    
class InviteList(APIView):
    def get(self, request, pk=None):

        try:
            user = UserProfile.objects.get(id=pk)
        except:
            return Response(data={"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        data = {}

        listOfInComingInvites = list(chain(Friend.objects.filter(user_1=user, status=1).values_list(
            'user_2', flat=True), Friend.objects.filter(user_2=user, status=0).values_list('user_1', flat=True)))
        listOfOutComingInvites = list(chain(Friend.objects.filter(user_1=user, status=0).values_list(
            'user_2', flat=True), Friend.objects.filter(user_2=user, status=1).values_list('user_1', flat=True)))

        for i in range(len(listOfInComingInvites)):
            listOfInComingInvites[i] = UserProfile.objects.get(id=listOfInComingInvites[i])

        for i in range(len(listOfOutComingInvites)):
            listOfOutComingInvites[i] = UserProfile.objects.get(id=listOfOutComingInvites[i])

        data["Incoming invites"] = UserProfileSerializer(listOfInComingInvites,many=True).data
        data['Outcoming invites'] = UserProfileSerializer(listOfOutComingInvites,many=True).data

        return Response(data=data)

class FriendView(viewsets.ViewSet):

    def list(self, request, pk=None):

        try:
            user = UserProfile.objects.get(id=pk)
        except:
            return Response(data={"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        
        listOfUsers = list(chain(Friend.objects.filter(user_1=user, status=2).values_list(
            'user_2', flat=True), Friend.objects.filter(user_2=user, status=2).values_list('user_1', flat=True)))
        
        for i in range(len(listOfUsers)):
            listOfUsers[i] = UserProfile.objects.get(id=listOfUsers[i])
        serializer = UserProfileSerializer(listOfUsers,many=True)
        return Response(data=serializer.data)
    def destroy(self,request,pk=None):
        
        user = request.data.get('user')

        if not UserProfile.objects.filter(id=user).exists() or not UserProfile.objects.filter(id=pk).exists():
            return Response(data={"detail":"Not found"},status=status.HTTP_404_NOT_FOUND)
        
        if Friend.objects.filter(user_1=user,user_2=pk,status=2).exists():
            Friend.objects.get(user_1=user,user_2=pk,status=2).delete()
            return Response(data=UserProfileSerializer(UserProfile.objects.get(id=pk)).data)
        
        if Friend.objects.filter(user_2=user,user_1=pk,status=2).exists():
            Friend.objects.get(user_2=user,user_1=pk,status=2).delete()
            return Response(data=UserProfileSerializer(UserProfile.objects.get(id=pk)).data)

        return Response(data={"detail":"Not found"},status=status.HTTP_404_NOT_FOUND)
    



class AcceptInvite(APIView):
    def post(self, request):

        inviter = request.data.get('inviter')
        accepter = request.data.get('accepter')

        try:
            obj = Friend.objects.get(user_1=inviter, user_2=accepter)
            if obj.status != 2:
                Friend.objects.filter(user_1=inviter, user_2=accepter).update(status=2)
                return Response(data=UserProfileSerializer(UserProfile.objects.get(id=request.data.get('accepter'))).data)
            else:
                return Response(data={"detail":"You are already friends"},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(data={"detail":"Not found"},status=status.HTTP_404_NOT_FOUND)
        
        

class GetStatus(APIView):
    def get(self,request,user=None,target=None):
        try:
            obj = Friend.objects.get(user_1=user, user_2=target)
            if obj.status == 2:
                return Response(data={"relationshipStatus":"Friends"})
            if obj.status == 0:
                return Response(data={"relationshipStatus":"Invite sended"})
            if obj.status == 1:
                return Response(data={"relationshipStatus":"Got an invite"})
        except:
            pass
        try:
            obj = Friend.objects.get(user_2=user, user_1=target)
            if obj.status == 2:
                return Response(data={"relationshipStatus":"Friends"})
            if obj.status == 0:
                return Response(data={"relationshipStatus":"Got an invite"})
            if obj.status == 1:
                return Response(data={"relationshipStatus":"Invite sended"})
        except:
            return Response(data={"detail":"Not found"},status=status.HTTP_404_NOT_FOUND)