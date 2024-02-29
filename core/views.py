from django.shortcuts import render,redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile,Like,Follower
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
from random import shuffle
from django.db.models import Q
from .models import Post
def check_setting(request):
    return Profile.objects.filter(user=request.user).exists()

@login_required(login_url='login')
def profile(request,id):
    if(not check_setting(request)):
        return redirect("settings")
    if(Profile.objects.filter(user__username=id).exists()):
        user=Profile.objects.filter(user__username=id).first()
        posts=Post.objects.filter(user__username=id)
        post=posts.count()
        follower=Follower.objects.filter(user__username=id).count()
      
        is_follower=Follower.objects.filter(user__username=id,followers=request.user).exists()

        return render(request,"profile.html",{'user':user,'post':post,"posts":posts,'id':id,'follower':follower,'is_follow':is_follower})
    
    else:
        return redirect("home")
    

@login_required(login_url='login')
def follow_home(request,id):
    if(not check_setting(request)):
        return redirect("settings")
    if not User.objects.filter(username=id).exists():
        return redirect("home")

    follower=Follower.objects.filter(user__username=id,followers=request.user)
    if follower.exists():
        follower.delete()
        return redirect(reverse("home"))

    else:
        user=User.objects.get(username=id)
        Follower.objects.create(user=user,followers=request.user)
        return redirect(reverse("home"))
        

@login_required(login_url='login')
def follow(request,id):
    if(not check_setting(request)):
        return redirect("settings")
    if not User.objects.filter(username=id).exists():
        return redirect("home")

    follower=Follower.objects.filter(user__username=id,followers=request.user)
    if follower.exists():
        follower.delete()
        return redirect(reverse("profile",args=[id]))

    else:
        user=User.objects.get(username=id)
        Follower.objects.create(user=user,followers=request.user)
        return redirect(reverse("profile",args=[id]))
        

@login_required(login_url='login')
def search(request):
    if(not check_setting(request)):
        return redirect("settings")
    if request.method=="POST":
        username=request.POST.get("username")
        user=Profile.objects.filter(user__username__contains=username)
        return render(request,"search.html",{'user':user,"username":username,"user_profile":Profile.objects.get(user=request.user).profile_img.url})
   
 
    
    
@login_required(login_url='login')
def like(request,id):
    if(not check_setting(request)):
        return redirect("settings")
        
    if request.method=="GET":
        post=Post.objects.filter(id=id)
        if not post.exists():
            return redirect("home")
        post=post.first()
        like=Like.objects.filter(post_id=id,user=request.user)
        if(like.exists()):
            like.delete()
            post.like=post.like-1
            post.save()
        else:
            Like.objects.create(post_id=id,user=request.user)
            post.like=post.like+1
            post.save()
            
        return redirect("home")


@login_required(login_url='login')
def upload(request):
    if(not check_setting(request)):
        return redirect("settings")
    if request.method=="POST":
        file=request.FILES.get("myfile")
        caption=request.POST.get("caption")
      
        if file and caption:
            Post.objects.create(user=request.user,caption=caption,image=file)


        return redirect("home")

    
def Ret_Usr(a):
    return a.user



@login_required(login_url='login')
def home(request):
    if(check_setting(request)):
        post=[]
        followed_user=Follower.objects.filter(followers=request.user)
        for x in followed_user:
            post+=Post.objects.filter(user=x.user)
        post+=Post.objects.filter(user=request.user)
        shuffle(post)
        user=Follower.objects.filter(followers=request.user)
        user_list=list(map(Ret_Usr,user))
        to_user=list(User.objects.all())
        to_user.remove(request.user)
        print(to_user)
        print(user_list)

        for x in user_list:
            if x in to_user:
                to_user.remove(x)
        profile=[]

        for x in to_user:
            profile+=Profile.objects.filter(user=x)
        
       



     
        
        
    



        
        return render(request,"index.html",{'post':post,'user':Profile.objects.get(user=request.user),'follow':profile})
    else:
        return redirect("settings")
    
    
@login_required(login_url='login')
def settings(request):
    if request.method=="GET":
        if not check_setting(request):
           
            return render(request,"setting.html")
        else:
            user=Profile.objects.filter(user=request.user)
            return render(request,"setting.html",{'data':user.first(),'is_data':True})
    elif request.method=="POST":
        about=request.POST.get("about")
        location=request.POST.get("location")
        file=request.FILES.get("image")
        if not(about and location and file):
            return redirect("settings")
        if not check_setting(request):
            user=Profile.objects.create(user=request.user,userid=request.user.pk,location=location,bio=about,profile_img=file)
        else:
            user=Profile.objects.filter(user=request.user).first()
            user.location=location
            user.bio=about
            user.profile_img=file
            user.save()
        return redirect("home")


        

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="GET":
        return render(request,"signup.html")
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("pass")
        cpass=request.POST.get("cpass")
        email=request.POST.get("cpass")
        if(not (username and password and cpass and email)):
            messages.error(request,"ALL FIELD IS REQUIRED")
            return redirect('signup')
        if not password==cpass:
            messages.error(request,"PASSWORD AND CONFIRM PASSWORD DOESNT MATCH")
            return redirect('signup')            
        user=User.objects.filter(username=username)
        if(user.exists()):
            messages.error(request,"Username already registered")
            return redirect('signup')
        else:
            user=User.objects.create(username=username,email=email)
            user.set_password(password)
            user.save()
            return redirect("login")

        
def logins(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="GET":
        return render(request,"signin.html")
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        if(not (username and password)):
            messages.error(request,"Enter username and password")
            return redirect('login')           
        user=authenticate(username=username,password=password)
        if(not user):
            messages.error(request,"Invalid Credentials")
            return redirect('login')
        else:
            login(request,user)
            return redirect('home')
        
def logouts(request):
    if not request.user.is_authenticated:
        return redirect('login')
    logout(request)
    messages.success(request,"LOgout Sucessfully")
    return redirect('login')






    