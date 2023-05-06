from django.urls import path
from . import views

urlpatterns = [
    path("invite/", views.InviteFriend.as_view(), name="inviteFriend"),# Инвайт в друзья
    path("friends/<int:user>/", views.ListFriends.as_view()), # Список друзей
    path("friends/<int:pk>", views.DeleteFriend.as_view()),# Удалить друга
    path("invite",views.ListInvites.as_view()),# Список инвайтов. В body: toUser - входящих, fromUser - исходящих
    path("acceptInvite/",views.AcceptInvite.as_view())#Принимает user_1 и user_2, пользователи, учавствующие в инвайте
]
