from django.shortcuts import render
from .models import FriendsOfFriends 
from django.http import JsonResponse
from django.contrib.auth.models import User

# Create your views here.
def AddFriends(request,uid, sid):
    if request.method=="POST":
        data={}
        user = User.objects.get(pk =uid)
        friends= User.objects.get(pk =sid)

        if FriendsOfFriends.objects.filter(user=user, friends=friends).exists():
            data['msg']="Request already sent"
        else:
            FriendsOfFriends.objects.create(
                user=user,
                friends= friends,
                status=1
            )
            data['msg']="Created Successfully"
        return JsonResponse(data)
    else:
        return JsonResponse({})
    
def AcceptRequest(request, sid, uid):
    # if request.method=="POST":
    data={}
    user = User.objects.get(pk =uid)
    friends= User.objects.get(pk =sid)
    if FriendsOfFriends.objects.filter(user=user, friends=friends).exists():
        a=FriendsOfFriends.objects.filter(user=user, friends=friends)
        a.update(
            status=2
        )
        data['msg']="Accepted Successfully"
        data['id']=a.first().id
    else:
        data["msg"]="Request is Error"
    return JsonResponse(data)