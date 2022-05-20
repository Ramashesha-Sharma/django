"""testStamp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from testRepositoryApp.views import ProjectViewSet, ApplicationModuleViewSet, TestCaseViewSet, TestScenarioViewSet
from testPlanApp.views import TestPlanViewSet, TestPlanExecutionViewSet, ApplicationVersionViewSet
# from rest_framework import views
from rest_framework.routers import DefaultRouter
# from knox import views as knox_views
# from accounts.views import LoginAPI, RegisterAPI
from rest_framework.authtoken.views import obtain_auth_token
 
router_testRepositry = DefaultRouter()
router_testPlan = DefaultRouter()
router_testRepositry.register('projects', ProjectViewSet)
router_testRepositry.register('applicationModules', ApplicationModuleViewSet)
router_testRepositry.register('testScenarios', TestScenarioViewSet)
router_testRepositry.register('testCases', TestCaseViewSet)
router_testPlan.register('testPlan', TestPlanViewSet)
router_testPlan.register('ApplicationVersion', ApplicationVersionViewSet)
router_testPlan.register('testPlanExecution', TestPlanExecutionViewSet) 
#router_testPlan.register('TestPlanReportsViewSet', TestPlanReportsViewSet) 
# router.register('file ', views.TestScenarioFileView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('testRepositry/',include(router_testRepositry.urls)),
    path('testPlan/',include(router_testPlan.urls)),
    path('api-token-auth/',obtain_auth_token,name="api_token_auth"),
    path('api-auth/', include('rest_framework.urls')),
    # path('flightServices/findFlights/',views.find_flight ),
    # path('flightServices/saveReservation/',views.save_reservation ),
    # path('api/register/', RegisterAPI.as_view(), name='register'),
    # path('api/login/', LoginAPI.as_view(), name='login'),
    # path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    # path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),

]