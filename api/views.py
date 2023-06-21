from django.shortcuts import render
import json
from django.http import JsonResponse, HttpResponse

# Create your views here.
from .many_views.getDatabaseStatsForIndexController import *


def getDatabaseStatsForIndexController(request):
    """
    GET statistics on the whole database
    :param request:
    :return: all relevant statistics ...
    """
    if request.method == "POST":
        res = {}

        tumor_types = get_tumor_types()
        if tumor_types is not None:
            res["tumor_types"] = tumor_types
        
        projects = get_projects_number()
        if projects is not None:
            res["projects"] = projects
        
        runs = get_runs_number()
        if runs is not None:
            res["runs"] = runs
        
        genera = get_genera_number()
        if genera is not None:
            res["genera"] = genera
        
        return JsonResponse(res)
    else:
        return JsonResponse({"code": "1002", "msg": f"{request.method} not supported"})
    
def getProjectSummaryForBarplot(request):
    """
    获取 explore 页面上用来画 project barplot 的数据
    """
    if request.method == "POST":
        sql="""
            select *, amplicon_16s + amplicon_ITS + WGS AS total 
            from project
            ORDER BY total DESC;
            """
        with connection.cursor() as cursor:
            cursor.execute(sql)
            res = dict_fetchall(cursor)
        if res is not None:
            return HttpResponse(json.dumps(res), content_type="application/json")

def getRunSummaryForBarplot(request):
    """
    获取 explore 页面上用来画 project barplot 的数据
    """
    if request.method == "POST":
        sql="""
            select distinct *
            from run
            ORDER BY total DESC;
            """
        with connection.cursor() as cursor:
            cursor.execute(sql)
            res = dict_fetchall(cursor)
        if res is not None:
            return HttpResponse(json.dumps(res), content_type="application/json")