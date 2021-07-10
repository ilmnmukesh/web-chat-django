
from django.urls import path
from . import views

urlpatterns = [
    path('<int:uid>/<int:sid>/', views.AddFriends, name='friendsOfFriends'),
    path("accept/<int:sid>/<int:uid>/", views.AcceptRequest, name="acceptFriendRequest")
]