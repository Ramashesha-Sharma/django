from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage  
from rest_framework import filters

from django.shortcuts import render

# Create your views here.
from testPlanApp.models import TestPlan, TestPlanExecution, ApplicationVersion
from testPlanApp.models import TestCase

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from testPlanApp.serializers import TestPlanSerializer, TestPlanExecutionSerializer, ApplicationVersionSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import filters
from rest_framework import status
from rest_framework.decorators import action

from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User

from testRepositoryApp.serializers import TestCaseSerializer, TestScenarioSerializer, ProjectSerializer
from itertools import chain

class ApplicationVersionViewSet(viewsets.ModelViewSet):
    queryset = ApplicationVersion.objects.all()
    serializer_class =  ApplicationVersionSerializer
    permission_classes = (IsAdminUser ,)


class TestPlanViewSet(viewsets.ModelViewSet):
    queryset = TestPlan.objects.all()
    serializer_class =  TestPlanSerializer


    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['project','version','description','created_by']
    search_fields = ['$description','$jira']
    ordering_fields = ['project','version','description','created_by','jira']


    permission_classes = [IsAuthenticated]





class TestPlanExecutionViewSet(viewsets.ModelViewSet):
    queryset  = TestPlanExecution.objects.all()
    serializer_class =  TestPlanExecutionSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status','testPlan']
    
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['name','description']

    permission_classes = (IsAuthenticated,)    
    def perform_create(self, serializer):
        request = serializer.context['request']
        serializer.save(updated_by=self.request.user,status="No Run",reason="Added New",)

    def perform_update(self, serializer):
        request = serializer.context['request']
        serializer.save(updated_by=self.request.user)
             
    
    @action(detail=False, methods = ['POST'] )
    def delete_multiple(self,request):
        data = request.data.get("ids").split(",")
        response = []
        for pk in data : 
            print(pk)
            try:
                testPlanExe = TestPlanExecution.objects.get(id = pk)
                testPlanExe.delete()
                response.append("1")
            except:
                response.append("0")

        return Response(response)


    @action(detail=False, methods = ['POST'] )
    def add_multiple(self,request):
        try :
            testcase = request.data.get("testcase").split(",")
            testplan = request.data.get("testplan")
            testproject = request.data.get("testproject").split(",")
            testcase_ids = []
            
            if "sanity" in testcase:
                for pk_new in testproject:
                    testcase_temp = TestCase.objects.all().filter(sanity=1,project=pk_new).values_list('id', flat=True)
                    testcase_ids = list(chain(testcase_ids, testcase_temp))
                    

            if "acceptance" in testcase:
                for pk_new in testproject:
                    testcase_temp = TestCase.objects.all().filter(acceptance=1,project=pk_new).values_list('id', flat=True)
                    testcase_ids = list(chain(testcase_ids, testcase_temp))
           
            if "regression" in testcase:
                for pk_new in testproject:
                    testcase_temp = TestCase.objects.all().filter(regression=1,project=pk_new).values_list('id', flat=True)
                    testctestcase_idsase = list(chain(testcase_ids, testcase_temp))
                    print("regression" + str(pk_new))

            if "automated" in testcase:
                for pk_new in testproject:
                    testcase_temp = TestCase.objects.all().filter(automated=1,project=pk_new).values_list('id', flat=True)
                    testcase_ids = list(chain(testcase_ids, testcase_temp))
                
            if "sanity" in testcase or  "acceptance" in testcase or "regression" in testcase or "automated" in testcase:
                testcase = testcase_ids

            testScenario_list = []
            for pk in testcase : 
         
                testScenario_list.append(
                    TestPlanExecution(
                        reason="Added New",
                        status = "No Run",
                        testPlan=TestPlan.objects.get(id = testplan),
                        testCase=TestCase.objects.get(id = pk),
                        updated_by=request.user
                    )
                )

            TestPlanExecution.objects.bulk_create(testScenario_list, ignore_conflicts=True)

            return Response("no check !!! SUCCESS")
        except Exception as e: # work on python 3.x
            return Response(str(e))
    


    @action(detail=False, methods = ['POST'] )
    def get_Report(self,request):
        response = {}
        try :
            testplan = request.data.get("testplan")

            pass_tc =TestPlanExecution.objects.filter(status = "Pass", testPlan = testplan)
            response["Pass"] = pass_tc.count()

            fail_tc =TestPlanExecution.objects.filter(status = "Fail",  testPlan = testplan)
            response["Fail"] = fail_tc.count()

            bloacked_tc =TestPlanExecution.objects.filter(status = "Blocked",  testPlan = testplan)
            response["Bloacked"] = bloacked_tc.count()

            norun_tc =TestPlanExecution.objects.filter(status = "No Run", testPlan = testplan)
            response["NoRun"] = norun_tc.count()

            response["Total"] = TestPlanExecution.objects.filter(testPlan = testplan).count()

            return Response(response)
        except Exception as e: 
            return Response(str(e))


