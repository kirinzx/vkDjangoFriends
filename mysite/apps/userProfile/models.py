from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=255,unique=True,error_messages={"unique":"This username is already used"})
    def __str__(self):
        return self.username