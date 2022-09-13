from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=300)
    email = models.CharField(max_length=100)
    private_key = models.CharField(max_length=100)

class Surveys(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    surveyname = models.CharField(max_length=100)
    surveyid = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    json = models.TextField()

class Accessable (models.Model):
    surveyid = models.CharField(max_length=100)
    emailList = models.CharField(max_length=20000)
    allowedbyall = models.BooleanField(default=False)

class Answer(models.Model):
    surveyid = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    json = models.TextField()
    anonymous = models.BooleanField(default=False)
    starttime = models.CharField(max_length=100)
    endtime = models.CharField(max_length=100)