from rest_framework  import serializers
from testRepositoryApp.models import Project, ApplicationModule, TestScenario, TestCase

from rest_framework import serializers



class ProjectListerializer(serializers.ListSerializer):
    def create(self, validated_data):
        project = [Project(**item) for item in validated_data]
        return Project.objects.bulk_create(project)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields =  '__all__'

    
class ApplicationModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationModule
        fields =  '__all__'


class TestScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestScenario
        fields =  '__all__'

    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        try :   
            if request.method == "GET":
                rep['project'] = ProjectSerializer(instance.project).data
                rep['application_module'] = ApplicationModuleSerializer(instance.application_module).data
        except :
            print("TS file upload")
        return rep



class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields =  '__all__'
    
    
    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        try :
            if request.method == "GET":
                rep['project'] = ProjectSerializer(instance.project).data
                rep['application_module'] = ApplicationModuleSerializer(instance.application_module).data
        except :
            print("TC file upload")
        return rep


