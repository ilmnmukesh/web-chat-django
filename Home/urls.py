
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('logout/', views.logOut, name='logout'),
    path('searchFriends/', views.searchFriendList, name="searchFriends"),
    path('getFriends/', views.getFriendList, name="getFriends"),
    path('showFriends/', views.showFriendsList, name="showFriendsList"),

    path('change/name/', views.changeUsername, name="change_username"),
    path('change/image/', views.changeImage, name="change_image"),
]