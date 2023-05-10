from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Relationship
from .serializers import RelationshipSerializer
from rest_framework.response import Response
from apps.userProfile.models import UserProfile
from apps.userProfile.serializers import UserProfileSerializer
from rest_framework import status
from itertools import chain

class ActionInvite(viewsets.ViewSet):

    def create(self, request):

        inviter = request.data.get("inviter")
        accepter = request.data.get("accepter")

        if inviter == accepter:
            return Response(data={"detail":"inviter can't be equal to accepter"},status=status.HTTP_400_BAD_REQUEST)

        if not UserProfile.objects.filter(id=inviter).exists() or not UserProfile.objects.filter(id=accepter).exists():
            return Response(data={"detail":"Not found"},status=status.HTTP_404_NOT_FOUND)

        if inviter == accepter:
            return Response(data={"detail": "You can't be your friend"}, status=status.HTTP_400_BAD_REQUEST)

        if Relationship.objects.filter(user_1=inviter, user_2=accepter, status=True).exists() or Relationship.objects.filter(user_1=accepter, user_2=inviter, status=True).exists():
            return Response(data={"detail": "You are already friends"}, status=status.HTTP_400_BAD_REQUEST)

        if Relationship.objects.filter(user_1=inviter, user_2=accepter, status=False).exists():
            return Response(data={"detail": "Invite is already created"}, status=status.HTTP_400_BAD_REQUEST)

        if Relationship.objects.filter(user_1=accepter, user_2=inviter, status=False).exists():
            Relationship.objects.filter(
                user_1=accepter, user_2=inviter, status=False).update(status=True)
            return Response(data={"successInvite": "Теперь вы друзья"})

        invite = Relationship.objects.create(user_1=UserProfile.objects.get(
            id=inviter), user_2=UserProfile.objects.get(id=accepter), status=False)
        serializer = RelationshipSerializer(invite)

        return Response(data=serializer.data)
    
    def update(self,request):

        inviter = request.data.get("inviter")
        accepter = request.data.get("accepter")
        action = request.data.get("action")

        if inviter == accepter:
            return Response(data={"detail":"inviter can't be equal to accepter"},status=status.HTTP_400_BAD_REQUEST)

        try:
            obj = Relationship.objects.get(user_1=inviter, user_2=accepter)
            if obj.status == False:
                if action == "accept":
                    Relationship.objects.filter(user_1=inviter, user_2=accepter).update(status=True)
                    return Response(data=UserProfileSerializer(UserProfile.objects.get(id=request.data.get('inviter'))).data)
                if action == 'decline':
                    Relationship.objects.get(user_1=inviter, user_2=accepter).delete()
                    return Response(data=UserProfileSerializer(UserProfile.objects.get(id=request.data.get('inviter'))).data)
                return Response(data={"detail":"invalid action field"},status=status.HTTP_400_BAD_REQUEST)
            
            return Response(data={"detail":"You are already friends"},status=status.HTTP_400_BAD_REQUEST)
        
        except:
            return Response(data={"detail":"Not found"},status=status.HTTP_404_NOT_FOUND)
        
class InviteList(APIView):
    def get(self, request, user_id=None):

        try:
            user = UserProfile.objects.get(id=user_id)
        except:
            return Response(data={"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        data = {}

        listOfOutComingInvites = list(Relationship.objects.filter(user_1=user, status=False).values_list('user_2', flat=True))
        listOfInComingInvites = list(Relationship.objects.filter(user_2=user, status=False).values_list('user_1', flat=True))

        for i in range(len(listOfInComingInvites)):
            listOfInComingInvites[i] = UserProfile.objects.get(id=listOfInComingInvites[i])

        for i in range(len(listOfOutComingInvites)):
            listOfOutComingInvites[i] = UserProfile.objects.get(id=listOfOutComingInvites[i])

        data["Входящие заявки"] = UserProfileSerializer(listOfInComingInvites,many=True).data
        data['Исходящие заявки'] = UserProfileSerializer(listOfOutComingInvites,many=True).data

        return Response(data=data)

class FriendList(APIView):

    def get(self, request, user_id=None):

        try:
            user = UserProfile.objects.get(id=user_id)
        except:
            return Response(data={"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        
        listOfUsers = list(chain(Relationship.objects.filter(user_1=user, status=True).values_list(
            'user_2', flat=True), Relationship.objects.filter(user_2=user, status=True).values_list('user_1', flat=True)))
        
        for i in range(len(listOfUsers)):
            listOfUsers[i] = UserProfile.objects.get(id=listOfUsers[i])
        serializer = UserProfileSerializer(listOfUsers,many=True)
        return Response(data=serializer.data)

class DeleteFriend(APIView):
     
     def delete(self,request,user_id=None,friend_id=None):

        if user_id == friend_id:
            return Response(data={"detail":"user_id can't be equal to friend_id"})
        
        if not UserProfile.objects.filter(id=friend_id).exists() or not UserProfile.objects.filter(id=user_id).exists():
            return Response(data={"detail":"Not found"},status=status.HTTP_404_NOT_FOUND)
        
        if Relationship.objects.filter(user_1=friend_id,user_2=user_id,status=True).exists():
            Relationship.objects.get(user_1=friend_id,user_2=user_id,status=True).delete()
            return Response(data=UserProfileSerializer(UserProfile.objects.get(id=friend_id)).data)
        
        if Relationship.objects.filter(user_2=friend_id,user_1=user_id,status=True).exists():
            Relationship.objects.get(user_2=friend_id,user_1=user_id,status=True).delete()
            return Response(data=UserProfileSerializer(UserProfile.objects.get(id=friend_id)).data)

        return Response(data={"detail":"Not found"},status=status.HTTP_404_NOT_FOUND)
class GetStatus(APIView):
    def get(self,request,user_id=None,target_id=None):
        if target_id == user_id:
            return Response(data={"detail":"user_id can't be equal to target_id"},status=status.HTTP_400_BAD_REQUEST)
        if UserProfile.objects.filter(id=user_id).exists() and UserProfile.objects.filter(id=target_id).exists():
            if Relationship.objects.filter(user_1=user_id, user_2=target_id).exists():
                obj = Relationship.objects.get(user_1=user_id, user_2=target_id)
                if obj.status == True:
                    return Response(data={"relationshipStatus":"Уже друзья"})
                if obj.status == False:
                    return Response(data={"relationshipStatus":"Есть исходящая заявка"})
            elif Relationship.objects.filter(user_2=user_id, user_1=target_id).exists():
                obj = Relationship.objects.get(user_2=user_id, user_1=target_id)
                if obj.status == True:
                    return Response(data={"relationshipStatus":"Уже друзья"})
                if obj.status == False:
                    return Response(data={"relationshipStatus":"Есть входящая заявка"})
            else:
                return Response(data={"relationshipStatis":"Нет ничего"})
        else:
            return Response(data={"detail":"Not found"},status=status.HTTP_404_NOT_FOUND)