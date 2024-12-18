from api.many_views.base import *
def getFeatureTableByProjectID(batch_id, kingdom):
    if kingdom == "bacteria":
        sql = """
            SELECT f.*
            FROM feature_table_bac f
            INNER JOIN sample_meta_curated s ON f.run_id = s.run_id
            WHERE s.batch = %s;
        """
    elif kingdom == "fungi":
        sql = """
            SELECT f.*
            FROM feature_table_fungi f
            INNER JOIN sample_meta_curated s ON f.run_id = s.run_id
            WHERE s.batch = %s;
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
        cursor.execute(sql, [ batch_id ])
        feature = dict_fetchall(cursor)
    return feature

def getBatchsByProjectID(project_id):
    sql="""
        SELECT DISTINCT project_id, batch, assay_type
        FROM sample_meta_curated
        WHERE project_id = %s;
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, [ project_id ])
        batchs = dict_fetchall(cursor)
    return batchs

def getStatsByProjectID(project_id):
    """
    获取项目的统计信息nr valid runs\ nr bacteria \ nr fungi \ related phenotype
    """
    # get related phenotype
    sql1="""
        select distinct phenotype_name, phenotype_id 
        from sample_meta_curated where project_id = %s;
    """
    # get nr valid runs, runs with bac, runs with fungi
    sql2="""
        SELECT
            count(*) AS total_run_count,
            SUM(CASE WHEN QC_state = 1 THEN 1  ELSE 0 END) AS valid_run_count,
            SUM(CASE WHEN QC_Bacteria = 1 THEN 1 ELSE 0 END) AS run_with_bac,
            SUM(CASE WHEN QC_Fungi = 1 THEN 1 ELSE 0 END) AS run_with_fungi,
            SUM(CASE WHEN QC_KOs = 1 THEN 1 ELSE 0 END) AS run_with_kos
        FROM sample_meta_curated WHERE project_id = %s;
    """
    # get DA stats
    """ ??? taxa from ??? batchs """
    sql3="""
        SELECT s.project_id, s.batch,
            r.da_id, r.marker_count, r.assay_type, r.case_name, r.control_name,
            sum(case when s.phenotype_name = r.case_name then 1 else 0 end) as case_run_count,
            sum(case when s.phenotype_name = r.control_name then 1 else 0 end) as control_run_count,
            sum(r.marker_count) OVER (PARTITION BY s.project_id) AS total_marker_count
        FROM (
            SELECT DISTINCT project_id, batch2 AS batch, phenotype_name, run_id
            FROM sample_meta_curated
            WHERE project_id = %s
        ) AS s
        INNER JOIN (
            SELECT da_id, batch, assay_type, case_name, control_name,
            COUNT(*) AS marker_count
            FROM da_results
            GROUP BY da_id, batch, assay_type, case_name, control_name
        ) AS r ON s.batch = r.batch
        GROUP BY s.project_id, s.batch,r.da_id, r.marker_count, r.assay_type, r.case_name, r.control_name;
    """
    stats = {}
    with connection.cursor() as cursor:
        cursor.execute(sql1, [ project_id ])
        phenotype = dict_fetchall(cursor)
        cursor.execute(sql2, [ project_id ])
        counts = dict_fetchall(cursor)
        cursor.execute(sql3, [ project_id ])
        da_stats = dict_fetchall(cursor)
    stats['phenotype'] = phenotype
    stats['counts'] = counts
    stats['da_stats'] = da_stats
    return stats