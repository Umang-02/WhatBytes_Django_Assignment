from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from authentication import settings 
from django.core.mail import EmailMessage,send_mail
from .helpers import send_forget_password_mail
from . models import *
import uuid
# Create your views here.

def home(request):
    if request.user.is_anonymous:
        return redirect('/signin')
    
    fname=request.user.first_name
    context={'firstname':fname}
    return render(request,"authentication/index.html",context)

def signup(request):
    #Checking if the method is post
    if request.method=="POST":

        #Extracting the details such as username,fname,lname email etc from the fields used in html
        username=request.POST['username']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request,"Username already exists: Please try any other username")
            return redirect("home")
        
        if User.objects.filter(email=email):
            messages.error(request,"Email has already been registered")
            return redirect("home")
        
        if pass1!=pass2:
            messages.error(request,"Passwords do not match, please try again!")

        if not username.isalnum():
            messages.error(request,"Username must be alpha-numeric")
            return redirect("home")

        myuser=User(username=username,email=email)
        myuser.set_password(pass1)
        myuser.save()

        profile_obj=Profile.objects.create(user=myuser)
        profile_obj.save()
        myuser.first_name=firstname
        myuser.last_name=lastname

        myuser.is_active=True
        myuser.save()

        messages.success(request,"Your account has been successfully created")

        return redirect("signin")

    return render(request,"authentication/signup.html")

def signin(request):

    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            firstname=user.first_name
            return render(request,"authentication/index.html",{'firstname':firstname})
        else:
            messages.error(request,"Username or password is incorrect")
            return redirect('home')
    if request.user.is_anonymous!=True:
        return redirect('/')
    return render(request,"authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request,"You have logged out successfully")
    return redirect('home')
    
def ForgetPassword(request):
    try:
        if request.method=='POST':
            username=request.POST['username']

            if not User.objects.filter(username=username):
                messages.error(request,"No such user found")
                return redirect('/signup')

            user_obj=User.objects.get(username=username)
            token=str(uuid.uuid4())
            profile_obj=Profile.objects.get(user=user_obj)
            profile_obj.forget_password_token=token
            profile_obj.save()
            send_forget_password_mail(user_obj.email,token)
            messages.success(request,"An email has been sent to reset the password")
            return redirect("forget-password")

    except Exception as e:
        print(e)
    return render(request,'authentication/forgetpassword.html')

def changePassword(request,token):
    context={}
    try:
        profile_obj=Profile.objects.filter(forget_password_token=token).first()
        
        if request.method=="POST":
            new_pass=request.POST['new_password']
            confirm_pass=request.POST['reconfirm_password']
            user_id=request.POST.get('user_id')
            if user_id is None:
                messages.error(request,'No user found')
                return redirect('/change-password/{token}')

            if new_pass!=confirm_pass:
                messages.error(request,"Passwords do not match.")
                return redirect('/change-password/{token}')
            
            user_obj=User.objects.get(id=user_id)
            user_obj.set_password(new_pass)
            user_obj.save()
            return redirect('/signin')

        context={'user_id':profile_obj.user.id}
    except Exception as e:
        print(e)
    return render(request,'authentication/changepassword.html',context)

def profile(request):
    if request.user.is_anonymous:
        return redirect('/signin')
    username=request.user.username
    email=request.user.email
    print(email)
    lastlogin=request.user.last_login
    context={'username':username,'email':email,'lastlogin':lastlogin}

    return render(request,'authentication/profilepage.html',context)