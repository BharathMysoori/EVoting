from django.shortcuts import HttpResponse, render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from config.settings import EMAIL_HOST_USER
from .models import *
from .emails import *
from django.core.mail import send_mail

# Create your views here.

@login_required(login_url='login')
def home(request):
    candata = candidate.objects.all()
    
   
    
    #usrdata = voter.objects.filter(user=request.user)
    loguser = request.user
    print('USER:',loguser.voter)
    print(loguser.voter.voted)
    if loguser.voter.voted:

        return render(request,'user/voted.html')
    if request.method=='POST':
        vote = request.POST.get('cvote')
        print(vote)
        if vote:
            messages.success(request,'YOU have voted')
            loguser.voter.voted = True
            loguser.voter.votedTo = vote
            loguser.save()
            return redirect('home')
    return render(request,'user/home.html',{'data':candata})

    
@user_passes_test(lambda user: not user.username, login_url='/', redirect_field_name=None)
def loginView(request):
    if request.method=='POST':
        
        vid = request.POST.get('vid')
        pwsd = request.POST.get('pswd')
        
        
        print(vid,pwsd)
    

        
        
        
        
        user = authenticate(request,username=vid,password=pwsd)
        print("user",user)
        if user is not None:
            try:
                otp = random.randint(1000,9999)
                otp = str(otp)
                usr = User.objects.get(username=vid)
                print(usr)
                usr.voter.otp = otp
                usr.save()
                subj = 'Login for Vote'

                msg = f'Your OTP:{otp} for login'
                send_mail(subj,msg,EMAIL_HOST_USER,[usr.email],fail_silently=False)
            except Exception as e:
                return render(request,'user/noconnection.html')
            

            login(request,user)
            print('loged in')
            messages.success(request, 'OTP sent to the mail id'+usr.email)
            return redirect('otp')
            #return render(request,'user/home.html')
        else:
            messages.error(request,'Username and Password Doesnt match Try again')
            return redirect('login')
    return render(request,'user/login.html')
        
        
        
@user_passes_test(lambda user: not user.username, login_url='/', redirect_field_name=None)
def register(request):
    if request.method=='POST':
        vid = request.POST.get('voterid')
        age = request.POST.get('voterage')   
        mid = request.POST.get('mailid')
        pwd = request.POST.get('pswd')
        wd = request.POST.get('ward')
        cty = request.POST.get('city')
        #otp = random.randint(1000,9999)
        #otp = str(otp)
        msg = f'Your OTP is:{otp}'
        if User.objects.filter(username=vid).exists():
            messages.info(request,'Username already exist')
            print("username")
            return render(request,'user/register.html')
        elif User.objects.filter(email=mid).exists():
            messages.info(request,'Email already taken')
            print('mail')
            return render(request,'user/register.html')
        else:
            newuser = User.objects.create_user(username=vid,email=mid,password=pwd)
            print("user saved")
            newuser.voter.city = cty
            newuser.voter.age = age
            newuser.voter.ward = wd
            #newuser.voter.otp = otp
            newuser.save()
            #send_mail('Register verification',msg,EMAIL_HOST_USER,[mid],fail_silently=False)
            print("voted id added")
            authenticate(request,username=vid,password=pwd)
            #messages.success(request, 'OTP Sent to the mail id')
            print('redircted otp.html')
            return redirect('login')
                
    else:
        return render(request,'user/register.html')

def otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        mail = request.POST.get('mail')
        uid = request.user
        usr = User.objects.get(id=uid.id)
        print(usr)
        print(usr.voter.verified)
        if otp == usr.voter.otp:
            usr.voter.verified = True
            usr.save()
            
            print('User verified-----')
            messages.success(request, 'User verified')
            return redirect('home')
        else:
            print(otp,usr.voter.otp)
            messages.error(request,'OTP invalid')
            return redirect('otp')
        
        
    return render(request,'user/otp.html')
                
   
            
            
def logoutView(request):
    logout(request)
    return redirect('login')
            
            
            
            
def profileView(request):
    data = voter.objects.filter(user=request.user)
    if request.method == 'POST':
        for d in data:
            d.dp = request.FILES.get('pic')
            d.save()
        print('PIC updated')
            
        

    return render(request,'user/userProfile.html',{'data':data})

            
            
    