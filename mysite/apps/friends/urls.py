from django.urls import path
from . import views

urlpatterns = [
    path("user/invite", views.ActionInvite.as_view({"post":"create","put":"update"})),# TESTED
    path("user/<int:user_id>/invite", views.InviteList.as_view()), # TESTED
    path("user/<int:user_id>/friend", views.FriendList.as_view()), # TESTED
    path("user/<int:user_id>/friend/<int:friend_id>",views.DeleteFriend.as_view()),
    path("user/<int:user_id>/target/<int:target_id>/status",views.GetStatus.as_view()), #TESTED
]
