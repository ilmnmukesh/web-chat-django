from Login.models import UserProfile
from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import json

def Default(request):
    if request.method == 'POST':
        if json.loads(request.POST['checkUsername']):    
            username= json.loads(request.POST.get('username')).strip()
            valid = True
            if User.objects.filter(username=username).exists():
                valid=False
            data ={'valid':valid}
            return JsonResponse(data) 
        elif json.loads(request.POST['signup']):   
            email= json.loads(request.POST.get('email'))
            username= json.loads(request.POST.get('username'))
            password= json.loads(request.POST.get('password'))
            valid=False
            if not(User.objects.filter(username=username).exists()):
                valid=True
                User.objects.create_user(username, email, password)
            data ={'valid':valid, 'username':username}
            return JsonResponse(data)
        else:
            username= json.loads(request.POST.get('username'))
            password= json.loads(request.POST.get('password'))
            if not(User.objects.filter(username=username).exists()):
                msg = 'User Name is not exists'
                usr, pwd='', ''
            elif not(User.objects.filter(username=username, password=password).exists()):
                msg='Password is incorrect'
                usr, pwd=username, ''
            else:
                msg, usr, pwd='','',''

            user = authenticate(request, username=username, password=password)
            valid=False
            if user is not None:
                valid=True
                login(request, user)
            data ={'valid':valid, 'msg':msg, 'username':usr, 'pwd':pwd}
            return JsonResponse(data)
    
    return render(request, 'default.html')

def ForgotPassword(request):
    if request.method=='POST':
        if json.loads(request.POST['usrExists']):
            username= json.loads(request.POST['username'])
            email = json.loads(request.POST['email'])
            valid=False
    
            if User.objects.filter(username=username).exists():
                if User.objects.filter(email=email).exists():
                    valid= True
                    msg=''
                else:
                    msg="Email is Does Not Exists"
            else:
                msg="Username is Incorrect"
                
            return JsonResponse({'msg':msg, 'valid':valid, 'username':username,'email':email})
        else:
            username=json.loads(request.POST['username'])
            email=json.loads(request.POST['email'])
            password= json.loads(request.POST['password'])
            cpassword = json.loads(request.POST['cpassword'])
            
            valid=False
            if User.objects.filter(username=username, email=email).exists():
                valid=True
                if cpassword==password:
                    user= User.objects.get(username=username, email=email)
                    user.set_password(password)
                    user.save()
                    msg='Password Changed Successfully'
                else:
                    msg="Password Miss Matching"
                    valid= False
            else:
                msg='Something Went Wrong Refresh to Continue'
    
            return JsonResponse({'msg':msg, 'valid':valid})
    return render(request, 'forgot_password.html')

def updateName(request):
    if request.method=="POST":
        curr = request.POST.get("current_name")
        name = request.POST.get("username")
        print(request.POST,request.user.username, curr)
        if request.user.username==curr:
            request.user.username=name
            request.user.save()
            return redirect("home")
        else:
            return render(request, "change_name.html", {"err":"Current Login user error"})
    return redirect("login")

def updateImage(request):
    if request.method=="POST":
        curr = request.POST.get("current_name")
        image = request.FILES["image"]
        if request.user.username==curr:
            try:
                old_image=request.user.userprofile.picture.path
            except:
                pass            
            obj, created=UserProfile.objects.update_or_create(user=request.user, defaults={"picture":image})
            if not created:
                import os
                try:
                    os.remove(old_image)
                except:
                    pass
            return redirect("home")
        else:
            return render(request, "change_name.html", {"err":"Current Login user error"})
    return redirect("login")

