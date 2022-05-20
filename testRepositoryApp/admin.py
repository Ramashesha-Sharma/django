from django.contrib import admin

from .models import TestCase, TestScenario, ApplicationModule, Project
# Register your models here.


admin.site.register(TestCase)
admin.site.register(TestScenario)
admin.site.register(ApplicationModule)
admin.site.register(Project)