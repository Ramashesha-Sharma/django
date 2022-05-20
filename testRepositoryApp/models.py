from django.db import models
from simple_history.models import HistoricalRecords

from django.contrib.auth import get_user_model
User = get_user_model()

import csv
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

# Create your models here.


class Project(models.Model):
    project = models.CharField(max_length=55, unique=True)
    description = models.TextField(blank=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.project
0
class ApplicationModule(models.Model):
    module = models.CharField(max_length=55, unique=True)
    description = models.TextField(blank=False)
    history = HistoricalRecords()
    def __str__(self):
        return self.module


class TestScenario(models.Model):
    name = models.CharField(max_length=55, unique=True)
    description = models.TextField(blank=False)
    
    created_by = models.ForeignKey(User, related_name="testscenarios_created_by",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add =True)
    
    updated_by = models.ForeignKey(User, blank=True, related_name="testscenarios_updated_by",on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    update_comments = models.TextField(blank=True, default='')

    application_module = models.ForeignKey(ApplicationModule, related_name="testscenarios_application_module",null=False, blank=False,on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name="testscenarios_project",null=False, blank=False,on_delete=models.CASCADE)
    
    jira = models.CharField(max_length=10)

    history = HistoricalRecords()

    def __str__(self):
        return self.name
        depth = 1



class TestCase(models.Model):
    
    name = models.CharField(max_length=55, unique=True)
    description = models.TextField(blank=False)
    
    created_by = models.ForeignKey(User, related_name="testcases",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    precondition =  models.CharField(max_length=512,blank=True, default='')
    testdata =  models.CharField(max_length=512,blank=True, default='')
    teststep = models.TextField(blank=False)
    expected = models.TextField(blank=False)

    updated_by = models.ForeignKey(User, blank=True, related_name="testcases_updated_by",on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    update_comments = models.TextField(blank=True, default='')

    automated  = models.BooleanField(default=False)
    sanity = models.BooleanField(default=False)
    acceptance = models.BooleanField(default=False)
    regression = models.BooleanField(default=False)

    jira = models.CharField(max_length=10)

    application_module = models.ForeignKey(ApplicationModule, related_name="testcases_application_module",null=False, blank=False,on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name="testcases_project",null=False, blank=False,on_delete=models.CASCADE)
    testscenario = models.ForeignKey(TestScenario, related_name="testcases_testscenario",null=False, blank=False,on_delete=models.CASCADE)
    
    history = HistoricalRecords()

    def __str__(self):
        return self.name
        depth = 1

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def createAuthToken(sender,instance,created,**kwargs):
    if created:
        Token.objects.create(user=instance)