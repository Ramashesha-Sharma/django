from django.db import models
from simple_history.models import HistoricalRecords
from testRepositoryApp.models import TestCase, Project


from django.contrib.auth import get_user_model
User = get_user_model()


# Create your models here.
class ApplicationVersion(models.Model):
    version = models.CharField(max_length=55, unique=True)
    releaseDate = models.DateField(blank=False)
    
    history = HistoricalRecords()
    def __str__(self):
        return self.version


class TestPlan(models.Model):
    project = models.ForeignKey(Project, related_name="testplan_project",null=False, blank=False,on_delete=models.CASCADE)
    version = models.ForeignKey(ApplicationVersion, related_name="testplan_application_version",null=False, blank=False,on_delete=models.CASCADE)
    description = models.TextField(blank=False)
    testCases = models.ManyToManyField(TestCase, through='TestPlanExecution')
    jira = models.CharField(max_length=10)

    created_by = models.ForeignKey(User, related_name="testplan_created_by",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add =True)
    history = HistoricalRecords()

    class Meta:
        unique_together = [['project','version']]

    def __int__(self):
        return self.id
        depth = 1


class TestPlanExecution(models.Model):
    testPlan = models.ForeignKey(TestPlan, on_delete=models.CASCADE)
    testCase = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    
    updated_by = models.ForeignKey(User, blank=True, related_name="testplanexe_updated_by",on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    reason = models.TextField(blank=False)

    STATUS_CHOICES = (
        ('No Run', 'No Run'),
        ('Pass', 'Pass'),
        ('Fail', 'Fail'),
        ('Blocked', 'Blocked'),
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES)


    class Meta:
        unique_together = [['testPlan','testCase']]
    
    def __str__(self):
        return self.id