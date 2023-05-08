from django.db import models
from apps.userProfile.models import UserProfile 

class Friend(models.Model):
    user_1 = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="user_1",default='')
    user_2 = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="user_2",default='')
    status = models.SmallIntegerField(null=True)


# status: 0 - user_1 -> user_2. 1 - user_1 <- user_2. 2 - friends