from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# router = DefaultRouter()
# router.register('dsp', views.DataSelectorProjectsViewSet)
# router.register('dsr', views.DataSelectorRunsViewSet)

urlpatterns = [
    path('getDatabaseStatsForIndexController/', views.getDatabaseStatsForIndexController),

    path('getProjectSummaryForBarplot/', views.getProjectSummaryForBarplot),
    path('getRunSummaryForBarplot/', views.getRunSummaryForBarplot),

    path('getTumorTypeToID/', views.getTumorTypeToID),

    path('getPhenotypeComparisons/', views.getPhenotypeComparisons),
    
    path('getProjectsandRuns/', views.getProjectsandRuns),
    path('getAllRunsAsync/', views.getAllRunsAsync),
]