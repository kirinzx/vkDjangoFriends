from django.urls import path
from . import views

urlpatterns = [
    path("invite", views.CreateInvite.as_view()),#inviter - id user'a, accepter - id user'a # TESTED
    path("invite/<int:pk>/", views.InviteList.as_view()), # TESTED
    path("friend/<int:pk>/", views.FriendView.as_view({"get":"list","delete":"destroy"})),#user # TESTED
    path("acceptInvite",views.AcceptInvite.as_view()),# Inviter, Accepter # TESTED
    path("status/<int:user>/<int:target>/",views.GetStatus.as_view()), #TESTED
]
