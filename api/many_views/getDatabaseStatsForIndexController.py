from api.many_views.base import *

def get_disease2term():
    sql = """
            select 
                count( distinct(run_id) ) as nr_assoc_runs 
            from 
                sample_to_run_info as t1, projects as t2 
            where 
                t1.disease = %s and t1.project_id = t2.Project_ID;"""
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return dict_fetchall(cursor)
    
def get_tumor_types():
    sql = """
        select count(short_name) from project 
        where short_name != 'health';
        """
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return cursor.fetchone()[0]

def get_projects_number():
    sql = """
        select count(distinct project_id) from project_all;
        """
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return cursor.fetchone()[0]

def get_runs_number():
    sql = """
        select count(distinct run_id) from sample_meta_curated;
        """
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return cursor.fetchone()[0]
    
def get_genera_number():
    sql = """
        # 统计 fungi 和 bacteria 的数量放到一个 sql 里面
        SELECT
            COUNT(CASE WHEN taxa LIKE '%k__Bacteria%' AND taxa LIKE '%|g__%' THEN 1 END) AS bacteria_count,
            COUNT(CASE WHEN taxa LIKE '%k__fungi%' AND taxa LIKE '%|g__%' THEN 1 END) AS fungi_count
        FROM
            feature_table;
        """
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return dict_fetchall(cursor)[0]