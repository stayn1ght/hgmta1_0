from api.many_views.base import *

def getProjectStats():
    sql = """
        select
            count(distinct project_id) as projects_number
        from project_all;
        """
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return dict_fetchall(cursor)[0]

def getRunStats():
    sql = """
        select
            count(distinct run_id) as runs_number,
            COUNT(CASE WHEN assay_type = "WGS" THEN 1 END) AS WGS_count,
            COUNT(CASE WHEN assay_type = "16S" THEN 1 END) AS amplicon_16s_count,
            COUNT(CASE WHEN assay_type = "ITS" THEN 1 END) AS amplicon_ITS_count
        from sample_meta_curated;
        """
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return dict_fetchall(cursor)[0]