from rest_framework.serializers import ModelSerializer
from .models import Relationship


class RelationshipSerializer(ModelSerializer):
    class Meta:
        model = Relationship
        fields = ("user_1", "user_2")
        depth = 1
    
