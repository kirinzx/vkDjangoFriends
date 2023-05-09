from django.db import models
from apps.userProfile.models import UserProfile 

class Relationship(models.Model):
    user_1 = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="user_1",default='')
    user_2 = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="user_2",default='')
    status = models.BooleanField(null=True)


# status: False - user_1 -> user_2. True - friends