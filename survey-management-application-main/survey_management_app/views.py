from django.shortcuts import render,redirect
from passlib.hash import sha512_crypt as sha512
from .models import User,Surveys,Accessable, Answer
import random
import string
from django.contrib import messages
from django.http import  JsonResponse
import os
from django.core.mail import send_mail


otp=""
# Create your views here.
def index(request):
    if 'SurveyapplicationPrivateKey' not in request.session:
        return render(request,'index.html',{'username':'Login'})
    else:
        if User.objects.filter(private_key=request.session['SurveyapplicationPrivateKey']).exists():
            user = User.objects.get(private_key=request.session['SurveyapplicationPrivateKey'])
            name = user.name
            return render(request,'index.html',{'username':name})
        else:
            return render(request,'index.html',{'username':'Login'})
    # # Checks if private key element is present in request.session
    # if 'SurveyapplicationPrivateKey' not in request.session:
    #     return redirect('login')
    # else:
    #     # If present now checks if private key is present in database
    #     if User.objects.filter(private_key=request.session['SurveyapplicationPrivateKey']).exists():
    #         # If yes User is logged in
    #         return redirect('home')
    #     else:
    #         return redirect('login')

def home(request):
    user = User.objects.get(private_key=request.session['SurveyapplicationPrivateKey'])
    email = user.email
    name=user.name
    survey = Surveys.objects.filter(email=email)
    recent = Surveys.objects.all().order_by('id')[:3][::-1]
    return render(request,'home.html',{'survey':survey,'username':name,'recent':recent})

def login(request):
    if 'SurveyapplicationPrivateKey' not in request.session:
        return render(request,'login.html')
    else:
        if User.objects.filter(private_key=request.session['SurveyapplicationPrivateKey']).exists():
            user = User.objects.get(private_key=request.session['SurveyapplicationPrivateKey'])
            name = user.name
            return redirect('home')
        else:
            return render(request,'login.html')

def signup(request):
    return render(request,'signup.html')

def signupuser(request):
    username=request.POST['name']
    email=request.POST['email']
    email =email.lower()
    pwd=request.POST['password']
    cpwd = request.POST['cpassword']
    if pwd != cpwd:
        messages.error(request, 'Passwords do not match')
        return redirect('signup')

    if User.objects.filter(email=email).exists():
            messages.info(request,'User Already Exists !')
            return redirect('signup')
    else:
            global otp
            otp=''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
            message="OTP : "+otp + "\n If you didn't did this please ignore this"
            reciever=[str(email)]
            subject="OTP for Survey Management"
            send_mail(subject,message,'enter_mail_here',reciever)
            return render(request,'otp.html',{'username':username,'email':email,'pwd':pwd})

def otpverifcation(request):
    otp_provided=request.POST['otp']
    username=request.POST['username']
    email=request.POST['email']
    pwd=request.POST['password']
    global otp
    if otp == otp_provided:
        print(pwd)
        pwd=sha512.hash(pwd, rounds=5000,salt="surveyforms")
        email=email.lower()
        User.objects.create(name=username,password=pwd,email=email,private_key="nill")
        return redirect('login')
    else :
        messages.info(request,'Wrong OTP !')
        return redirect('signup')

def loginuser(request):
    email=request.POST['email']
    pwd1=request.POST['password']
    email=email.lower()
    if User.objects.filter(email=email).exists():
        user=User.objects.get(email=email)
        password_verify=user.password
        print(pwd1)
        pwd1=sha512.hash(pwd1, rounds=5000,salt="surveyforms")
        print(pwd1)
        print(password_verify)
        if pwd1==password_verify:
            privatekey=''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(30))
            request.session['SurveyapplicationPrivateKey']=privatekey
            user.private_key=privatekey
            user.save()
            return redirect('home')
        else:
            messages.info(request,'Wrong Password !')
            return redirect('login')
    else:
        messages.info(request,'User Does Not Exists !')
        return redirect('login')

def newform(request):
    user = User.objects.get(private_key=request.session['SurveyapplicationPrivateKey'])
    email = user.email
    name=user.name
    return render(request, 'newform.html',{'username':name , 'email':email})

def sendsurveyback(request):
    surveyname=request.GET['surveyname']
    surveydesc=request.GET['surveydescription']
    json=request.GET['json']
    user = User.objects.get(private_key=request.session['SurveyapplicationPrivateKey'])
    email = user.email
    name = user.name
    surveyid=''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(30))
    Surveys.objects.create(surveyid=surveyid,name=name,surveyname=surveyname,description=surveydesc,json=json,email=email)
    return JsonResponse('home', safe=False)

survyeidglobal = 1
def opensurvey(request):
    surveyid=request.GET['surveyid']
    global survyeidglobal
    survyeidglobal=surveyid
    return JsonResponse('opensurveyhtml', safe=False)

def opensurveyhtml(request):
    global survyeidglobal
    user = User.objects.get(private_key=request.session['SurveyapplicationPrivateKey'])
    email = user.email
    username = user.name
    survey = Surveys.objects.get(id = survyeidglobal)
    data = str(survey.json)
    if Accessable.objects.filter(surveyid=survyeidglobal).exists():
        allowed = Accessable.objects.get(surveyid=survyeidglobal)
        emailList = allowed.emailList
        emailList = emailList[:-1]
        emaillist = emailList.split(",")
        return render(request,'opensurvey.html',{'survey':survey,'username':username,'data':data,'emaillist':emaillist})
    else:
        return render(request,'opensurvey.html',{'survey':survey,'username':username,'data':data})

def updatesurvey(request):
    surveyname=request.GET['surveyname']
    surveydesc=request.GET['surveydescription']
    json=request.GET['json']
    surveyid = request.GET['surveyid']
    user = User.objects.get(private_key=request.session['SurveyapplicationPrivateKey'])
    email = user.email
    name = user.name
    surveyid=''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(30))
    Surveys.objects.update(surveyid=surveyid,name=name,surveyname=surveyname,description=surveydesc,json=json,email=email)
    return JsonResponse('home', safe=False)

def deletesurvey(request):
    surveyid = request.GET['surveyid']
    Surveys.objects.get(id=surveyid).delete()
    return JsonResponse('home', safe=False)

def logout(request):
    del request.session['SurveyapplicationPrivateKey']
    return redirect('login')

def responses(request):
    return render(request,'reponses.html')

def sendshareinfoback(request):
    surveyid=request.GET['surveyid']
    emaillist=request.GET['emaillist']
    allowed = request.GET['allowed'] 
    if allowed == 'true':
        allowed = True
    else:
        allowed = False
    if Accessable.objects.filter(surveyid=surveyid).exists():
            Accessable.objects.update(surveyid=surveyid,emailList = emaillist, allowedbyall = allowed)
    return JsonResponse('opensurveyhtml', safe=False)
    
def takesurvey(request,surveyid):
    if surveyid == 'sendansback':
        json=request.GET['json']
        email = request.GET['email']
        anonymous = request.GET['anonymous']
        surveyid = request.GET['surveyid']
        starttime = request.GET['starttime']
        endtime = request.GET['endtime']
        print(starttime+" "+endtime)
        message = "Hello some users have taken your survey "+surveyid+". Please find the link below.\n\n"
        send_mail('Survey', message, 'Sending Email Here', ['admin email here'], fail_silently=False)
        if anonymous == 'false':
            message = "Thank you for filling out survey"
            send_mail('Survey', message, 'Sending Email Here', [email], fail_silently=False)
        Answer.objects.create(surveyid = surveyid, json = json, email = email, anonymous = anonymous,starttime = starttime, endtime = endtime)
        return redirect('home')
    else:
    # Check if user is allowed if not then login page and see a way to come back to this page
        survey = Surveys.objects.get(id = surveyid)
        access = Accessable.objects.get(surveyid=surveyid)
        # After logged in get user email too 
        return render(request,'takesurvey.html',{'surveyid':surveyid,'survey':survey,'accessable':access.allowedbyall,'emaillist':access.emailList})

def contact(request):
    return render(request,'contact.html')

def contactusform(request):
    name = request.POST['name']
    email = request.POST['email']
    message = request.POST['message']
    subject = request.POST['subject']
    email = email.lower()
    message = name+" "+email+" "+message
    send_mail(subject,message,'enter_mail_here',['enter_mail_here'])
    return render(request,'contact.html')

def sendansback(request,surveyid):
        json=request.GET['json']
        email = request.GET['email']
        anonymous = request.GET['anonymous']
        surveyid = request.GET['surveyid']
        starttime = request.GET['starttime']
        endtime = request.GET['endtime']
        print(starttime+" "+endtime)
        message = "Hello some users have taken your survey "+surveyid+". Please find the link below.\n\n"
        send_mail('Survey', message, 'Sending Email Here', ['admin email here'], fail_silently=False)
        if anonymous == 'false':
            message = "Thank you for filling out survey"
            send_mail('Survey', message, 'Sending Email Here', [email], fail_silently=False)
        Answer.objects.create(surveyid = surveyid, json = json, email = email, anonymous = anonymous,starttime = starttime, endtime = endtime)
        return redirect('home')

def responses(request,surveyid):
    responses = Answer.objects.filter(surveyid = surveyid)
    return render(request,'responses.html',{'responses':responses})

def viewresponses(request,responseid):
    response = Answer.objects.get(id = responseid)
    return render(request, 'viewresponse.html',{'response':response})

def cronjob(request):
    message = "Hello some users have taken your survey . Please Login and check status\n This is an automatically scheduled task\n\n"
    send_mail('Survey', message, 'Sending Email Here', ['admin email here'], fail_silently=False)
    return JsonResponse('home', safe=False)