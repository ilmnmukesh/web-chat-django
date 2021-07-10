from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.serializers import serialize
from Login.models import UserProfile
from Friends.models import FriendsOfFriends
from django.db.models import Q
import json
from django.contrib.auth import logout

DEFAULT_IMAGE='/static/img/one.png'

# Create your views here.
def viewFriends(request:HttpRequest):
    data={'requestList':[]}
    users=FriendsOfFriends.objects.filter(Q(user= request.user)|Q(friends=request.user), status=2)
    for user in users:
        temp={}
        temp['id']=user.id
        
        if request.user.username==user.user.username:
            u = User.objects.get(pk = user.friends.id)    
            temp['friend']=user.friends.username.capitalize()
            try:
                temp['img'] = UserProfile.objects.get(user__pk=user.friends.id).picture.url
            except UserProfile.DoesNotExist:
                temp['img']=DEFAULT_IMAGE
            temp['frd_id']=user.friends.id
        else:
            u = User.objects.get(pk = user.user.id)
            temp['friend']=user.user.username.capitalize()
            try:
                temp['img'] = UserProfile.objects.get(user__pk=user.user.id).picture.url
            except UserProfile.DoesNotExist:
                temp['img']=DEFAULT_IMAGE
            temp['frd_id']=user.user.id
        
        up=UserProfile(user=u)
        temp['last_seen']=up.last_seen()
        temp['online'] = up.online()
        data['requestList'].append(temp)
    return data

def Home(request):
    if not request.user.is_authenticated:
        return redirect("login")
    name=request.user.username.capitalize()
    friends = viewFriends(request)
    
    return render(request, 'home.html', {'name':name, 'friends':friends})

def searchFriendList(request):
    if request.method=="POST":
        username=json.loads(request.POST['q'])
    else:
        username =''
    data={'users':[]}

    users= User.objects.filter(username__icontains=username).exclude(username=request.user.username)
    for user in users:
        temp={}
        temp['id']=user.id
        temp['btn_info']=0
        if FriendsOfFriends.objects.filter(user=request.user.id, friends=user.id).exists():
            temp['btn_info']=FriendsOfFriends.objects.filter(user=request.user.id, friends=user.id).first().status
        elif FriendsOfFriends.objects.filter(user=user.id, friends=request.user.id).exists():
            temp['btn_info']=FriendsOfFriends.objects.filter(user=user.id, friends=request.user.id).first().status
        try:
            temp['img'] = UserProfile.objects.get(user=user.id).picture.url
        except UserProfile.DoesNotExist:
            temp['img']=DEFAULT_IMAGE
        temp['username']=user.username.capitalize()

        data['users'].append(temp)
    data['user_id']=request.user.id
    return JsonResponse(data)

def getFriendList(request):
    if request.method=="POST":
        data ={"requestList":[]}
        req= FriendsOfFriends.objects.filter(friends=request.user, status=1)
        for user in req:
            temp={}
            temp['id']=user.id
            temp['uid']=user.user.id
            temp['sid']= user.friends.id
            
            if request.user.username==user.user.username:
                temp['request_name']=1
                temp['sent_name']=user.friends.username.capitalize()
                
            else:
                temp['request_name']=0
                temp['sent_name']=user.user.username.capitalize()
                
            try:
                temp['img'] = UserProfile.objects.get(user=temp['sid']).picture.url
            except UserProfile.DoesNotExist:
                temp['img']=DEFAULT_IMAGE
            data["requestList"].append(temp)
        return JsonResponse(data)

def showFriendsList(request):
    data=viewFriends(request)
    return JsonResponse(data)

def logOut(request):
    logout(request)
    return redirect("login")

def changeUsername(request:HttpRequest):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "change_name.html") 

def changeImage(request:HttpRequest):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "add_image.html")    
