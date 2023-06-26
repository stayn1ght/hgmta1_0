from django.shortcuts import render
import json
from django.http import JsonResponse, HttpResponse

# Create your views here.
from .many_views.getDatabaseStatsForIndexController import *
from .many_views.getStatsByPhenotype import *
from .many_views.getProjectandRunStats import *

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
        
def getTumorTypeToID(request):
    """
    获取explore页面用于展示癌症缩写到全称和ID的映射
    """
    if request.method == "POST":
        sql="""
            select * from disease_info;
            """
        with connection.cursor() as cursor:
            cursor.execute(sql)
            res = dict_fetchall(cursor)
        if res is not None:
            return HttpResponse(json.dumps(res), content_type="application/json")
        
def getPhenotypeComparisons(request):
    """
    获取 differential abundance 数据
    """
    if request.method == "POST":
        data = json.loads(request.body)
        mesh_id = data.get("mesh_id", "")
        res = {}
        stats = get_run_summary_by_phenotype(mesh_id)
        alldata = get_all_data_of_phenotype_comparison(mesh_id)
        projects = get_marker_counts_by_project(mesh_id)
        if len(stats) > 0:
            res["stats"] = stats
        else:
            return JsonResponse(
                {
                    "code": "1002",
                    "msg": f"No data has been found for {mesh_id}",
                }
            )
        if len(projects) > 0:
            res["projects"] = projects
        if len(alldata) > 0:
            res["alldata"] = alldata
        return JsonResponse(res)
    else:
        return JsonResponse({"code": "1002", "msg": f"{request.method} not supported"})
    
def getProjectsandRuns(request):
    if request.method == "POST":
        sql1 = """
            select * from project_all;
            """
        sql2 = """
            select * from run;
            """
        projects_number = getProjectStats()
        run_stats = getRunStats()
        with connection.cursor() as cursor:
            cursor.execute(sql1)
            res1 = dict_fetchall(cursor)
            cursor.execute(sql2)
            res2 = dict_fetchall(cursor)
        if res1 is not None and res2 is not None:
            return JsonResponse({"projects": res1, "runs": res2, "projects_number": projects_number, "run_stats": run_stats})
        
def getAllRunsAsync(request):
    if request.method == "POST":
        try:
            if request.body:
                data = json.loads(request.body)
            else:
                data = {"limit": 10, "skip": 0}
            limit = int(data.get("limit", 10))
            skip = int(data.get("skip", 0))
            sql = """
                select * from sample_meta_curated limit %s, %s;
            """
            with connection.cursor() as cursor:
                cursor.execute(sql, [ skip, limit ])
                res = dict_fetchall(cursor)
            if res is not None:
                return HttpResponse(json.dumps(res), content_type="application/json")
        except:
            return JsonResponse({"code": "1002", "msg": "数据获取异常"})
    else:
        return JsonResponse({"code": "1002", "msg": f"{request.method} not supported"})
        
    