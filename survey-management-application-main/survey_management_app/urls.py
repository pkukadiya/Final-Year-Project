from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
     path('', views.index,name='index'),
     path('index', views.index,name='index'),
     path('home',views.home,name='home'),
     path('contact',views.contact,name='contact'),
     path('login',views.login,name='login'),
     path('logout',views.logout,name='logout'),
     path("loginuser", views.loginuser, name="loginuser"),
     path('signup',views.signup,name='signup'),
     path('signupuser',views.signupuser,name='signupuser'),
     path('otpverifcation',views.otpverifcation,name='otpverifcation'),

     path('newform',views.newform,name='newform'),
     path('sendsurveyback',views.sendsurveyback,name='sendsurveyback'),
     path('opensurvey',views.opensurvey,name='opensurvey'),
     path('opensurveyhtml',views.opensurveyhtml,name='opensurveyhtml'),
     path('updatesurvey',views.updatesurvey,name='updatesurvey'),
     path('deletesurvey',views.deletesurvey,name='deletesurvey'),
     path('responses',views.responses,name='responses'),
     path('sendshareinfoback',views.sendshareinfoback,name='sendshareinfoback'),
     path('takesurvey/<str:surveyid>/sendansback',views.sendansback,name='sendansback'),
     path('responses/<str:surveyid>',views.responses,name='responses'),
     path('responses/viewresponse/<str:responseid>',views.viewresponses,name='viewresponses'),
     path('takesurvey/<str:surveyid>',views.takesurvey,name='takesurvey'),
     path('contactusform',views.contactusform,name='contactusform'),

]