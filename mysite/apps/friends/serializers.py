from rest_framework.serializers import ModelSerializer
from .models import Friend


class FriendSerializer(ModelSerializer):
    class Meta:
        model = Friend
        fields = ("user_1", "user_2")
        depth = 1
    
