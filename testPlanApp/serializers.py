from rest_framework  import serializers
from testPlanApp.models import TestPlan, TestPlanExecution, ApplicationVersion
from testRepositoryApp.models import TestCase
from testRepositoryApp.serializers import TestCaseSerializer, TestScenarioSerializer, ProjectSerializer

from rest_framework import serializers




class ApplicationVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationVersion
        fields =  '__all__'


class TestPlanExecutionSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(TestPlanExecutionSerializer, self).__init__(many=many, *args, **kwargs)
        
    class Meta:
        model = TestPlanExecution
        fields =  '__all__'

    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        try :   
            if request.method == "GET":
                rep['testCase'] = TestCaseSerializer(instance.testCase).data
        except :
            pass
        return rep



class TestPlanSerializer(serializers.ModelSerializer):
    testCases = serializers.SerializerMethodField()
    class Meta:
        model = TestPlan
        fields =  '__all__'

    def get_testCases(self, obj):
        # obj is a Test Plan instance. Returns list of dicts
        qset = TestPlanExecution.objects.filter(testPlan=obj)
        
        return [TestPlanExecutionSerializer(m).data for m in qset]

    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        try :
            if request.method == "GET":
                rep['project'] = ProjectSerializer(instance.project).data
                rep['version'] = ApplicationVersionSerializer(instance.version).data
        except :
            pass
        return rep