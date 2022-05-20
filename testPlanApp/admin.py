from django.contrib import admin
from .models import TestPlan, TestPlanExecution, ApplicationVersion
# Register your models here.


admin.site.register(TestPlan)
admin.site.register(TestPlanExecution)
admin.site.register(ApplicationVersion)
