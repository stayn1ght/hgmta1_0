from django.shortcuts import render
import json
from django.http import JsonResponse, HttpResponse

# Create your views here.
from .many_views.getDatabaseStatsForIndexController import *
from .many_views.getStatsByPhenotype import *
from .many_views.getProjectandRunStats import *
from .many_views.getDataByProjectID import *

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
        
        """ genera = get_genera_number()
        if genera is not None:
            res["genera"] = genera """
        
        return JsonResponse(res)
    else:
        return JsonResponse({"code": "1002", "msg": f"{request.method} not supported"})

def searchable(request):
    """
    get data for selector in header
    """
    if request.method == "POST":
        sql="""select * from searchable order by keywords;"""
        res = {}
        with connection.cursor() as cursor:
            cursor.execute(sql)
            res['data'] = dict_fetchall(cursor)
        if res is not None:
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
            SELECT d.*, p.project_count, r.run_count,
            COALESCE(m.marker_count, 0) as marker_count
            FROM disease_info d
            JOIN (
                SELECT short_name, amplicon_16s + amplicon_ITS + WGS AS project_count
                FROM project
            ) p ON d.short_name = p.short_name
            JOIN (
                SELECT distinct short_name, total as run_count
                FROM run
            ) r ON d.short_name = r.short_name
            LEFT JOIN (
                SELECT case_name, count(distinct taxa) as marker_count
                from da_results
                group by case_name
            ) m ON d.phenotype_name = m.case_name
            ORDER BY r.run_count DESC;
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
            select 
                project_all.project_id, assay_type, project_title, project_description,
                public_accession, journal, processed_runs, total_runs, related_phenotypes, related_phenotype_ids
            from project_all
            left join (
                select
                    project_id,
                    sum(case when QC_state = 1 then 1 else 0 end) as processed_runs,
                    count(*) as total_runs
                from sample_meta_curated
                group by project_id
            ) as t1 on project_all.project_id = t1.project_id
            left join (
                select distinct project_id, 
                group_concat(distinct phenotype_name separator ';') as related_phenotypes,
                group_concat(distinct phenotype_id separator ';') as related_phenotype_ids
                from sample_meta_curated
                group by project_id
            ) as t2 on project_all.project_id = t2.project_id
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
        
def getProjectDetailsByID(request):
    if request.method == "POST":
        try:
            if request.body:
                data = json.loads(request.body)
                project_id = data.get("project_id", "")
                sql = """
                    select * from project_all 
                    LEFT JOIN (
                        select 
                            project_id, 
                            associated_project as associated_project_id 
                        from project_summary
                    ) as t1 on project_all.project_id = t1.project_id
                    left join (
                        select distinct
                            project_id, phenotype_name, phenotype_id
                        from sample_meta_curated
                        where phenotype_name != "Health"
                    ) as t2 on project_all.project_id = t2.project_id
                    where t1.project_id = %s;

                """
                with connection.cursor() as cursor:
                    cursor.execute(sql, [ project_id ])
                    res = dict_fetchall(cursor)[0]
                if res is not None:
                    return HttpResponse(json.dumps(res), content_type="application/json")
            else:
                return JsonResponse({"code": "1002", "msg": "数据获取异常"})
            
        except:
            return JsonResponse({"code": "1002", "msg": "数据获取异常"})

def getAllRunsByProjectIDAsync(request):
    if request.method == "POST":
        try:
            if request.body:
                data = json.loads(request.body)
                project_id = data.get("project_id", "")
                sql = """
                    select * from sample_meta_curated where project_id = %s;
                """
                with connection.cursor() as cursor:
                    cursor.execute(sql, [ project_id ])
                    res = dict_fetchall(cursor)
                if res is not None:
                    return HttpResponse(json.dumps(res), content_type="application/json")
            else:
                return JsonResponse({"code": "1002", "msg": "数据获取异常"})
            
        except:
            return JsonResponse({"code": "1002", "msg": "数据获取异常"})

def getProjectSummaryByDisease(request):
    if request.method == "POST":
        try:
            if request.body:
                data = json.loads(request.body)
                disease = data.get("mesh_id", "")
                sql = """
                    SELECT p.*, pp.phenotype_id, pp.assay_type
                    FROM project_summary p
                    JOIN (
                        SELECT distinct project_id, phenotype_id, assay_type
                        FROM sample_meta_curated 
                        WHERE phenotype_id = %s
                    ) pp ON p.project_id = pp.project_id;
                """
                with connection.cursor() as cursor:
                    cursor.execute(sql, [ disease ])
                    res = dict_fetchall(cursor)
                if res is not None:
                    return HttpResponse(json.dumps(res), content_type="application/json")
            else:
                return JsonResponse({"code": "1002", "msg": "只支持POST请求"})
            
        except:
            return JsonResponse({"code": "1002", "msg": "数据获取异常"})

def getDaResultsByDisease(request):
    if request.method == "POST":
        try:
            if request.body:
                data = json.loads(request.body)
                disease = data.get("mesh_id", "")
                sql = """
                select * from da_results
                left join (
                    select distinct phenotype_name, phenotype_id from sample_meta_curated
                    ) as t1 on da_results.case_name = t1.phenotype_name
                where phenotype_id = %s;
                """
                with connection.cursor() as cursor:
                    cursor.execute(sql, [ disease ])
                    res = dict_fetchall(cursor)
                if res is not None:
                    return HttpResponse(json.dumps(res), content_type="application/json")
            else:
                return JsonResponse({"code": "1002", "msg": "只支持POST请求"})
            
        except:
            return JsonResponse({"code": "1002", "msg": "数据获取异常"})
        
def getDataByProjectID(request):
    """
    获取 data/_id 页面需要的全部数据
    """
    if request.method == "POST":
        try:
            if request.body:
                data = json.loads(request.body)
                project_id = data.get("project_id", "")
                res = {}
                stats = getStatsByProjectID(project_id)
                batchs = getBatchsByProjectID(project_id)
                # feature = getFeatureTableByProjectID(project_id)
                if len(stats) > 0:
                    res["stats"] = stats
                if len(batchs) > 0:
                    res["batchs"] = batchs
                if res is not None:
                    return JsonResponse(res)
            else:
                return JsonResponse({"code": "1002", "msg": "只支持POST请求"})
        except:
            return JsonResponse({"code": "1002", "msg": "data access error"})

def getMetadataAllRuns(request):
    """
    获取所有runs的metadata 
      """
    if request.method == "POST":
        sql = """
        select * from sample_meta_curated;
        """
    with connection.cursor() as cursor:
            cursor.execute(sql)
            res = dict_fetchall(cursor)
    if res is not None:
        return HttpResponse(json.dumps(res), content_type="application/json")

def getProjectFeatureTable(request):
    """ 
     为 data/_id 页面提供 feature table 数据, 分别提供 bacteria 和 fungi 的丰度表
    """
    if request.method == "POST":
        if request.body:
            data = json.loads(request.body)
            project_id = data.get("project_id", "")
            kingdom = data.get("kingdom", "")
            if kingdom == "bacteria":
                sql = """
                    SELECT ftb.* 
                    FROM feature_table_bac ftb 
                    INNER JOIN sample_meta_curated smc ON ftb.run_id = smc.run_id 
                    WHERE smc.project_id = %s 
                    AND (ftb.taxa LIKE '%%|g__%%' OR ftb.taxa LIKE '%%|s__%%');
                """
            elif kingdom == "fungi":
                sql = """
                    SELECT ftb.* 
                    FROM feature_table_fungi ftb 
                    INNER JOIN sample_meta_curated smc ON ftb.run_id = smc.run_id 
                    WHERE smc.project_id = %s
                    AND (ftb.taxa LIKE '%%|g__%%' OR ftb.taxa LIKE '%%|s__%%');
                """
            elif kingdom == "ko":
                sql = """
                    SELECT ftb.* 
                    FROM feature_table_kos ftb
                    WHERE ftb.run_id IN (
                        SELECT run_id
                        FROM sample_meta_curated
                        WHERE project_id = %s
                    );
                """
            with connection.cursor() as cursor:
                cursor.execute(sql, [ project_id ])
                res = dict_fetchall(cursor)
            if res is not None:
                return HttpResponse(json.dumps(res), content_type="application/json")

def getFeatureTableByProjectID(request):
    """
    是对上述 getDataByProjectID 的一个补充,
    根据 batch, kingdom 获取要下载的 feature table
    每个project可能对应多个batch，需要根据batch来对应runs和feature table
    feature table 分为 bacteria 和 fungi 两个表
    """
    if request.method == "POST":
        try:
            if request.body:
                data = json.loads(request.body)
                batch_id = data.get("batch_id", "")
                kingdom = data.get("kingdom", "")
                feature = getFeatureTableByProjectID(batch_id, kingdom)
                if feature is not None:
                    return HttpResponse(json.dumps(feature), content_type="application/json")
            else:
                return JsonResponse({"code": "1002", "msg": "data access error"})
        except:
            return JsonResponse({"code": "1002", "msg": "只支持POST请求"})
        
def getMarkerTaxaByDAID(request):
    """
    根据 提供的 da_id 获取 marker taxa
    """
    if request.method == "POST":
        if request.body:
            data = json.loads(request.body)
            da_id = data.get("da_id", "")
            sql = """
                select * from da_results where da_id = %s
                order by lfc asc;
            """
            with connection.cursor() as cursor:
                cursor.execute(sql, [ da_id ])
                res = dict_fetchall(cursor)
            if res is not None:
                return JsonResponse({ da_id: res })
        else:
            return JsonResponse({"code": "1002", "msg": "data access error"})

def getPhenotypeID2Name(request):
    """
    根据 phenotype_id 获取 phenotype_name
    是对 phenotype/phenotype_id 页面的一个补丁
    """
    if request.method == "POST":
        if request.body:
            data = json.loads(request.body)
            phenotype_id = data.get("phenotype_id", "")
            sql = """
                select phenotype_name 
                from sample_meta_curated where phenotype_id = %s
                limit 1;
            """
            with connection.cursor() as cursor:
                cursor.execute(sql, [ phenotype_id ])
                res = dict_fetchall(cursor)
            if res is not None:
                return HttpResponse(json.dumps(res), content_type="application/json")
        else:
            return JsonResponse({"code": "1002", "msg": "data access error"})
        
def getFeatureTable(request):
    """
    提供给help页面的feature table下载
    """
    if request.method == "POST":
        sql="""
            # 合并 bac 和 fungi 的 feature table。bac和fungi的feature table的列名是一样的
            (select * from feature_table_bac limit 100)
            union all
            (select * from feature_table_fungi limit 100)
            union all
            (select id, ko as taxa, run_id, abundance from feature_table_kos limit 100);
        """
        with connection.cursor() as cursor:
            cursor.execute(sql)
            res = dict_fetchall(cursor)
        if res is not None:
            return HttpResponse(json.dumps(res), content_type="application/json")
        
def getDaResults(request):
    """
    提供给help页面下载da_results
    """
    if request.method == "POST":
        sql="""
            select * from da_results;
        """
        with connection.cursor() as cursor:
            cursor.execute(sql)
            res = dict_fetchall(cursor)
        if res is not None:
            return HttpResponse(json.dumps(res), content_type="application/json")
        
def getTaxa2NCBI(request):
    """
    提供给 project id 页面下载 taxa2ncbi 表格
    提供给 help 页面下载taxa2ncbi表格
    """
    if request.method == "POST":
        sql="""
            select * from taxa2ncbi;
        """
        with connection.cursor() as cursor:
            cursor.execute(sql)
            res = dict_fetchall(cursor)
        if res is not None:
            return HttpResponse(json.dumps(res), content_type="application/json")

def getTumorRank(request):
    """ 
    for explore page tumor rank bar-plot
    """
    if request.method == "POST":
        sql1 = """
            select * from gmtd;
        """
        sql2 = """
            select * from gmtp;
        """
        with connection.cursor() as cursor:
            cursor.execute(sql1)
            res1 = dict_fetchall(cursor)
            cursor.execute(sql2)
            res2 = dict_fetchall(cursor)
        if res1 is not None and res2 is not None:
            return JsonResponse({"gmtd": res1, "gmtp": res2})
    