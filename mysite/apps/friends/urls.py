from django.urls import path
from . import views

urlpatterns = [
    path("invite/", views.InviteFriend.as_view({"post":"create"}), name="inviteFriend"),# Инвайт в друзья, в body: toUser - кому, fromUser - от кого
    path("friends/<int:user>/", views.ListFriends.as_view({"get":"list"})), # Список друзей
    path("friends/<int:pk>", views.DeleteFriend.as_view()),# Удалить друга
    path("invite",views.ListInvites.as_view()),# Список инвайтов. В body: toUser - входящих, fromUser - исходящих
    path("acceptInvite/",views.AcceptInvite.as_view()),#Принимает user_1 и user_2, пользователи, учавствующие в инвайте
    path("getStatus/<int:pk>",views.GetStatus.as_view({'get': 'retrieve'})),
]
