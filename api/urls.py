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

    path('getProjectDetailsByID/', views.getProjectDetailsByID),
    path('getAllRunsByProjectIDAsync/', views.getAllRunsByProjectIDAsync),

    path('getProjectSummaryByDisease/', views.getProjectSummaryByDisease),

    path('getDaResultsByDisease/', views.getDaResultsByDisease),

    path('searchable/', views.searchable),

    path('getDataByProjectID/', views.getDataByProjectID),
    path('getFeatureTableByProjectID/', views.getFeatureTableByProjectID),
    path('getMarkerTaxaByDAID/', views.getMarkerTaxaByDAID),

    path('getPhenotypeID2Name/', views.getPhenotypeID2Name),

    # data 页面下载 metadata of all runs
    path("getMetadataAllRuns/", views.getMetadataAllRuns),
    # data id 页面下载feature table
    path('getProjectFeatureTable/', views.getProjectFeatureTable),
    # help 页面下载数据的api
    path('getFeatureTable/', views.getFeatureTable),
    path('getDaResults/', views.getDaResults),
    path('getTaxa2NCBI/', views.getTaxa2NCBI),

]