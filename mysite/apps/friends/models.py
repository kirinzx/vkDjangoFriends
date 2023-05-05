from django.db import models
from apps.userProfile.models import UserProfile 

class Friend(models.Model):
    user_1 = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="user_1",default='')
    user_2 = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="user_2",default='')


class Invite(models.Model):
    fromUser = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="fromUser")
    toUser = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="toUser")
