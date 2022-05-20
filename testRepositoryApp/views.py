import csv
import codecs
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage  
from rest_framework import filters

from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated, IsAdminUser 
from testRepositoryApp.models import Project, ApplicationModule, TestScenario, TestCase
from testRepositoryApp.serializers import ProjectSerializer, ApplicationModuleSerializer, TestScenarioSerializer, TestCaseSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import filters
from rest_framework import status
from rest_framework.decorators import action

from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User

from typing import List

import csv
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage


fs = FileSystemStorage(location='tmp/')


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class =  ProjectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    permission_classes = (IsAdminUser ,)
 
class ApplicationModuleViewSet(viewsets.ModelViewSet):
    queryset = ApplicationModule.objects.all()
    serializer_class =  ApplicationModuleSerializer
    permission_classes = (IsAdminUser ,)

    
class TestScenarioViewSet(viewsets.ModelViewSet):
    queryset  = TestScenario.objects.all()
    serializer_class =  TestScenarioSerializer
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id','name','description','created_by','application_module','jira','project']
    search_fields = ['$name','$description','$jira']
    ordering_fields = ['name','description','created_by','updated_by','application_module','jira','project','created_at','updated_at',]

    permission_classes = (IsAuthenticated ,)
    def perform_create(self, serializer):
        request = serializer.context['request']
        serializer.save(created_by=self.request.user,updated_by=self.request.user)

    def perform_update(self, serializer):
        request = serializer.context['request']
        serializer.save(created_by=serializer.instance.created_by,created_at=serializer.instance.created_at,updated_by=self.request.user)

    @action(detail=False, methods = ['POST'] )
    def delete_multiple(self,request):
        ids = request.data.get("ids").split(",")
        response = []
        for pk in ids : 
            print(pk)
            try:
                testscenario = TestScenario.objects.get(id = pk)
                testscenario.delete()
                response.append("1")
            except:
                response.append("0")

        return Response(response)

    @action(detail=False, methods = ['POST'] )
    def upload_data(self,request):
        file = request.FILES.get("file")

        reader = csv.DictReader(codecs.iterdecode(file, "utf-8"), delimiter=",")
        data = list(reader)

        serializer = self.serializer_class(data=data, many=True)
        serializer.is_valid(raise_exception=True)

        testScenario_list = []
        for row in serializer.data:
            testScenario_list.append(
                TestScenario(
                    name=row["name"],
                    description=row["description"],
                    update_comments=row["update_comments"],
                    application_module_id=row["application_module"],
                    jira =row["jira"],
                    created_by = self.request.user,
                    updated_by = self.request.user,
                    project_id = row["project"],
                )
            )

        TestScenario.objects.bulk_create(testScenario_list)

        return Response("Successfully upload the data")


        content = file.read()
        
        file_content = ContentFile(content)

        file_name = fs.save("_temp.csv", file_content)


        
class TestCaseViewSet(viewsets.ModelViewSet):
    queryset  = TestCase.objects.all()
    serializer_class =  TestCaseSerializer



    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id','name','created_by','application_module','project', 'created_by', 'automated', 'testscenario','sanity', 'acceptance', 'regression']
    search_fields = ['$name','$description','$jira','$precondition','$testdata','$teststep','$expected',]
    ordering_fields = ['name','description','created_by','automated','sanity', 'acceptance', 'regression', 'testscenario',  'jira',  'updated_by','application_module','jira','project','created_at','updated_at',]
    
    permission_classes = (IsAuthenticated,)    
    def perform_create(self, serializer):
        request = serializer.context['request']
        serializer.save(created_by=self.request.user,updated_by=self.request.user)

    def perform_update(self, serializer):
        request = serializer.context['request']
        serializer.save(created_by=serializer.instance.created_by,created_at=serializer.instance.created_at,updated_by=self.request.user)
    

    @action(detail=False, methods = ['POST'] )
    def delete_multiple(self,request):
        data = request.data.get("ids").split(",")
        response = []
        for pk in data : 
            print(pk)
            try:
                testcase = TestCase.objects.get(id = pk)
                testcase.delete()
                response.append("1")
            except:
                response.append("0")

        return Response(response)


    @action(detail=False, methods = ['POST'] )
    def upload_data(self,request):
        file = request.FILES.get("file")

        reader = csv.DictReader(codecs.iterdecode(file, "utf-8"), delimiter=",")
        data = list(reader)

        serializer = self.serializer_class(data=data, many=True)
        serializer.is_valid(raise_exception=True)

        testCase_list = []
        for row in serializer.data:
            testCase_list.append(
                TestCase(
                    name=row["name"],
                    description=row["description"],
                    precondition=row["precondition"],
                    testdata=row["testdata"],
                    teststep=row["teststep"],
                    expected=row["expected"],

                    update_comments=row["update_comments"],
                    automated=row["automated"],
                    sanity=row["sanity"],
                    acceptance=row["acceptance"],
                    regression=row["regression"],

                    testscenario_id=row["testscenario"],
                    jira =row["jira"],

                    created_by = self.request.user,
                    updated_by = self.request.user,
                    application_module_id=row["application_module"],
                    project_id = row["project"],
                )
            )

        TestCase.objects.bulk_create(testCase_list)

        return Response("Successfully upload the data")